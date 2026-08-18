#!/usr/bin/env python3
"""Validate a WAB brand assessment without external dependencies."""

import json
import sys
from pathlib import Path


LENSES = {
    "position_and_difference",
    "audience_and_choice_barrier",
    "proof_and_credibility",
    "experience_and_consistency",
    "knowledge_and_workflow",
    "commercial_signal_and_learning",
}
GATES = {"true", "relevant", "ownable", "deliverable"}
ROUTES = {"open_self_serve", "professional_diagnosis", "enterprise_system"}


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def validate(data):
    errors = []
    required = {
        "assessment_version", "brand", "decision", "research_status",
        "evidence_ledger", "lens_scores", "primary_bottleneck",
        "differentiation_hypothesis", "next_30_days", "commercial_route",
        "limitations",
    }
    require(required <= set(data), f"missing top-level fields: {sorted(required - set(data))}", errors)
    if errors:
        return errors

    require(data["assessment_version"] == "1.0", "assessment_version must be 1.0", errors)
    evidence = data.get("evidence_ledger", [])
    ids = [item.get("id") for item in evidence]
    require(len(ids) == len(set(ids)), "evidence IDs must be unique", errors)
    known_ids = set(ids)

    scores = data.get("lens_scores", {})
    require(set(scores) == LENSES, "lens_scores must contain exactly the six WAB lenses", errors)
    for name, lens in scores.items():
        score = lens.get("score")
        require(isinstance(score, int) and 0 <= score <= 3, f"{name}.score must be an integer from 0 to 3", errors)
        for evidence_id in lens.get("evidence_ids", []):
            require(evidence_id in known_ids, f"{name} references unknown evidence ID {evidence_id}", errors)

    bottleneck = data.get("primary_bottleneck", {})
    require(bottleneck.get("lens") in LENSES, "primary_bottleneck.lens must be a WAB lens", errors)
    require(bool(bottleneck.get("statement")), "primary_bottleneck.statement is required", errors)
    for evidence_id in bottleneck.get("evidence_ids", []):
        require(evidence_id in known_ids, f"primary_bottleneck references unknown evidence ID {evidence_id}", errors)

    hypothesis = data.get("differentiation_hypothesis", {})
    gates = hypothesis.get("gates", {})
    require(set(gates) == GATES, "differentiation_hypothesis.gates must contain exactly four gates", errors)
    for name, gate in gates.items():
        require(gate.get("result") in {"pass", "partial", "fail"}, f"gate {name} has invalid result", errors)
        for evidence_id in gate.get("evidence_ids", []):
            require(evidence_id in known_ids, f"gate {name} references unknown evidence ID {evidence_id}", errors)

    next_steps = data.get("next_30_days", {})
    require(bool(next_steps.get("human_decisions")), "next_30_days must include at least one human decision", errors)
    require(bool(next_steps.get("do_not_automate")), "next_30_days must include at least one do-not-automate item", errors)
    require(data.get("commercial_route") in ROUTES, "commercial_route is invalid", errors)
    require(bool(data.get("limitations")), "limitations must not be empty", errors)
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_assessment.py path/to/assessment.json")
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
    print(f"Evidence items: {len(data['evidence_ledger'])}")
    print("Six lenses: 6/6")
    print("Differentiation gates: 4/4")
    print(f"Route: {data['commercial_route']}")


if __name__ == "__main__":
    main()
