#!/usr/bin/env python3
"""Validate a WAB Interview-to-Story package without external dependencies."""

import json
import sys
from pathlib import Path


ROUTES = {"person_story", "place_choice_story"}
SOURCE_KINDS = {"audio", "video", "transcript", "notes", "public_source", "brand_asset", "portrait"}
SOURCE_STATUS = {"available", "missing", "restricted"}
RIGHTS_STATUS = {"confirmed", "limited", "unknown", "not_required"}
EVIDENCE_TYPES = {"fact", "direct_quote", "paraphrase", "editorial_inference", "public_context"}
VERIFICATION = {"confirmed", "pending", "conflict", "excluded"}
PUBLICATION = {"allowed", "draft_only", "blocked"}
STORY_STATUS = {"draft", "verified", "approved"}
DELIVERY_STATUS = {"draft", "reviewed", "approved", "published"}
VISUAL_STATUS = {"draft", "generated", "reviewed", "approved", "published"}
GATE_RESULTS = {"pending", "pass", "fail", "approved", "rejected"}
REQUIRED_GATES = {
    "transcript_review",
    "fact_and_quote_review",
    "direction_approval",
    "translation_review",
    "image_rights_review",
    "final_publication",
}


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def unique_ids(items, label, errors):
    ids = [item.get("id") for item in items]
    require(all(isinstance(item_id, str) and item_id for item_id in ids), f"{label} IDs must be non-empty strings", errors)
    require(len(ids) == len(set(ids)), f"{label} IDs must be unique", errors)
    return set(ids)


def validate(data):
    errors = []
    required = {
        "package_version", "project", "source_register", "evidence_ledger",
        "canonical_story", "deliverables", "visuals", "gates", "limitations",
    }
    require(required <= set(data), f"missing top-level fields: {sorted(required - set(data))}", errors)
    if errors:
        return errors

    require(data["package_version"] == "1.0", "package_version must be 1.0", errors)
    project = data.get("project", {})
    route = project.get("route")
    require(route in ROUTES, "project.route must be person_story or place_choice_story", errors)
    for field in ("name", "story_id", "source_language"):
        require(bool(project.get(field)), f"project.{field} is required", errors)
    require(bool(project.get("target_languages")), "project.target_languages must not be empty", errors)

    sources = data.get("source_register", [])
    source_ids = unique_ids(sources, "source", errors)
    for source in sources:
        require(source.get("kind") in SOURCE_KINDS, f"source {source.get('id')} has invalid kind", errors)
        require(source.get("status") in SOURCE_STATUS, f"source {source.get('id')} has invalid status", errors)
        require(source.get("rights_status") in RIGHTS_STATUS, f"source {source.get('id')} has invalid rights_status", errors)

    available_kinds = {source.get("kind") for source in sources if source.get("status") == "available"}
    if route == "person_story":
        require(bool({"transcript", "notes"} & available_kinds), "person_story requires an available transcript or interview notes", errors)
    if route == "place_choice_story":
        require("public_source" in available_kinds, "place_choice_story requires at least one available public_source", errors)

    evidence = data.get("evidence_ledger", [])
    evidence_ids = unique_ids(evidence, "evidence", errors)
    evidence_by_id = {item.get("id"): item for item in evidence}
    for item in evidence:
        item_id = item.get("id")
        require(item.get("type") in EVIDENCE_TYPES, f"evidence {item_id} has invalid type", errors)
        require(item.get("verification") in VERIFICATION, f"evidence {item_id} has invalid verification", errors)
        require(item.get("publication") in PUBLICATION, f"evidence {item_id} has invalid publication state", errors)
        require(bool(item.get("locator")), f"evidence {item_id} requires a locator", errors)
        for source_id in item.get("source_ids", []):
            require(source_id in source_ids, f"evidence {item_id} references unknown source {source_id}", errors)
        require(bool(item.get("source_ids")), f"evidence {item_id} requires at least one source_id", errors)

    story = data.get("canonical_story", {})
    require(story.get("status") in STORY_STATUS, "canonical_story.status is invalid", errors)
    require(bool(story.get("route_rationale")), "canonical_story.route_rationale is required", errors)
    require(bool(story.get("core_question")), "canonical_story.core_question is required", errors)
    require(bool(story.get("core_thesis")), "canonical_story.core_thesis is required", errors)
    require(story.get("human_approval") in {"pending", "approved", "rejected"}, "canonical_story.human_approval is invalid", errors)
    if story.get("status") == "approved":
        require(story.get("human_approval") == "approved", "approved canonical story requires human_approval=approved", errors)

    deliverables = data.get("deliverables", [])
    unique_ids(deliverables, "deliverable", errors)
    for item in deliverables:
        item_id = item.get("id")
        require(bool(item.get("channel")), f"deliverable {item_id} requires channel", errors)
        require(bool(item.get("language")), f"deliverable {item_id} requires language", errors)
        require(bool(item.get("format")), f"deliverable {item_id} requires format", errors)
        require(item.get("status") in DELIVERY_STATUS, f"deliverable {item_id} has invalid status", errors)
        for evidence_id in item.get("evidence_ids", []):
            require(evidence_id in evidence_ids, f"deliverable {item_id} references unknown evidence {evidence_id}", errors)
            if item.get("status") in {"approved", "published"} and evidence_id in evidence_by_id:
                linked = evidence_by_id[evidence_id]
                require(linked.get("verification") == "confirmed", f"approved deliverable {item_id} uses unconfirmed evidence {evidence_id}", errors)
                require(linked.get("publication") == "allowed", f"approved deliverable {item_id} uses non-public evidence {evidence_id}", errors)
        require(bool(item.get("evidence_ids")), f"deliverable {item_id} requires evidence_ids", errors)

    visuals = data.get("visuals", [])
    unique_ids(visuals, "visual", errors)
    for item in visuals:
        item_id = item.get("id")
        require(item.get("rights_status") in RIGHTS_STATUS, f"visual {item_id} has invalid rights_status", errors)
        require(item.get("status") in VISUAL_STATUS, f"visual {item_id} has invalid status", errors)
        for evidence_id in item.get("evidence_ids", []):
            require(evidence_id in evidence_ids, f"visual {item_id} references unknown evidence {evidence_id}", errors)
        if item.get("status") in {"approved", "published"}:
            require(item.get("rights_status") in {"confirmed", "not_required"}, f"approved visual {item_id} requires confirmed or not_required rights", errors)

    gates = data.get("gates", {})
    require(set(gates) == REQUIRED_GATES, "gates must contain exactly the six required gates", errors)
    for name, result in gates.items():
        require(result in GATE_RESULTS, f"gate {name} has invalid result", errors)
    if story.get("status") in {"verified", "approved"}:
        require(gates.get("fact_and_quote_review") == "pass", "verified or approved story requires fact_and_quote_review=pass", errors)
    if story.get("status") == "approved":
        require(gates.get("direction_approval") == "approved", "approved story requires direction_approval=approved", errors)
    if any(item.get("status") in {"approved", "published"} for item in deliverables if item.get("language") != project.get("source_language")):
        require(gates.get("translation_review") == "pass", "approved translated deliverables require translation_review=pass", errors)
    if any(item.get("status") in {"approved", "published"} for item in visuals):
        require(gates.get("image_rights_review") == "pass", "approved visuals require image_rights_review=pass", errors)
    if any(item.get("status") == "published" for item in deliverables + visuals):
        require(gates.get("final_publication") == "approved", "published items require final_publication=approved", errors)

    require(bool(data.get("limitations")), "limitations must not be empty", errors)
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_story_package.py path/to/story-package.json")
        raise SystemExit(2)
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read valid JSON: {exc}")
        raise SystemExit(1)
    errors = validate(data)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("PASS")
    print(f"Route: {data['project']['route']}")
    print(f"Sources: {len(data['source_register'])}")
    print(f"Evidence items: {len(data['evidence_ledger'])}")
    print(f"Deliverables: {len(data['deliverables'])}")
    print(f"Visuals: {len(data['visuals'])}")


if __name__ == "__main__":
    main()
