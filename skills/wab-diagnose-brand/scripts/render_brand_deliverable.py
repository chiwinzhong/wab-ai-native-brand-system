#!/usr/bin/env python3
"""Validate and render a local website or editorial HTML review proof. No network I/O."""

import argparse
import base64
import datetime
import html
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path, PureWindowsPath

SKILL = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((SKILL / "references/production-brief.schema.json").read_text())
TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "number": (int, float)}


def check_schema(value, schema, where, errors):
    if "$ref" in schema:
        target = SCHEMA
        for key in schema["$ref"].split("/")[1:]:
            target = target[key]
        return check_schema(value, target, where, errors)
    kind = schema.get("type")
    if kind and (not isinstance(value, TYPES[kind]) or kind == "number" and isinstance(value, bool)):
        errors.append(f"{where}: expected {kind}")
        return
    if "const" in schema and value != schema["const"]:
        errors.append(f"{where}: must be {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{where}: invalid choice")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{where}.{key}: required")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value.keys() - properties.keys():
                errors.append(f"{where}.{key}: unknown field")
        for key in value.keys() & properties.keys():
            check_schema(value[key], properties[key], f"{where}.{key}", errors)
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", sys.maxsize):
            errors.append(f"{where}: invalid item count")
        for index, item in enumerate(value):
            check_schema(item, schema.get("items", {}), f"{where}[{index}]", errors)
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{where}: empty text")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{where}: invalid text format")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value) or value < schema.get("minimum", -float("inf")) or value > schema.get("maximum", float("inf")):
            errors.append(f"{where}: number out of range")


def asset_file(record, root):
    name = record["path"]
    path = Path(name)
    if path.is_absolute() or PureWindowsPath(name).is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
        raise ValueError("asset path must be relative, without traversal or remote URLs")
    root = Path(root).resolve()
    target = (root / path).resolve(strict=True)
    if not target.is_relative_to(root) or not target.is_file():
        raise ValueError("asset escapes its approved root")
    raw = target.read_bytes()
    if len(raw) > 5 * 1024 * 1024:
        raise ValueError("asset exceeds 5 MiB review-proof limit")
    suffix = target.suffix.lower()
    if suffix == ".svg":
        if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
            raise ValueError("SVG declarations/entities are not allowed")
        svg = ET.fromstring(raw)
        for node in svg.iter():
            if node.tag.rsplit("}", 1)[-1] in {"script", "foreignObject", "image"}:
                raise ValueError("SVG contains active or externally sourced content")
            for key, value in node.attrib.items():
                key = key.rsplit("}", 1)[-1].lower()
                if key.startswith("on") or key == "href" and not value.startswith("#"):
                    raise ValueError("SVG event/external reference is not allowed")
                targets = re.findall(r"url\(([^)]*)\)", value, re.I)
                if re.search(r"@import", value, re.I) or any(not target.strip().strip("'\"").startswith("#") for target in targets):
                    raise ValueError("SVG external styles are not allowed")
            if node.tag.rsplit("}", 1)[-1] == "style":
                raise ValueError("use explicit SVG presentation attributes, not style blocks")
        mime = "image/svg+xml"
    elif suffix == ".png" and raw.startswith(b"\x89PNG\r\n\x1a\n"):
        mime = "image/png"
    elif suffix in {".jpg", ".jpeg"} and raw.startswith(b"\xff\xd8\xff"):
        mime = "image/jpeg"
    elif suffix == ".webp" and raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        mime = "image/webp"
    else:
        raise ValueError("unsupported or invalid image file")
    return target, mime, raw


def validate(data, root, kind):
    errors = []
    check_schema(data, SCHEMA, "brief", errors)
    if errors:
        return errors
    if data["mode"] not in {kind, "both"}:
        errors.append("requested kind is not enabled by brief.mode")
    if kind not in data:
        errors.append(f"{kind}: required for requested output")
        return errors
    for collection in ["evidence", "assets"]:
        ids = [x["id"] for x in data[collection]]
        if len(ids) != len(set(ids)):
            errors.append(f"{collection}: duplicate IDs")
    evidence = {x["id"]: x for x in data["evidence"]}
    assets = {x["id"]: x for x in data["assets"]}
    for item in data["evidence"]:
        try:
            datetime.date.fromisoformat(item["as_of"])
        except ValueError:
            errors.append(f"{item['id']}: invalid as_of date")
        if item["classification"] == "synthetic" and not data["is_synthetic"]:
            errors.append("synthetic evidence requires is_synthetic=true")
    review = data["review"]
    if review["content_status"] == "approved":
        if not all(review[x].strip() for x in ["reviewer", "reviewed_at", "record_ref"]):
            errors.append("approved content requires reviewer, time and record")
    pages = data[kind]["pages"]
    ids = [p["id"] for p in pages]
    if len(ids) != len(set(ids)):
        errors.append("page IDs must be unique")
    if kind == "website" and "review-contact" in ids:
        errors.append("review-contact is reserved for the proof contact-state section")
    for page in pages:
        for p in page["paragraphs"]:
            refs = p["evidence_ids"]
            if p["kind"] in {"fact", "observation"} and not refs:
                errors.append(f"{page['id']}: factual/observation paragraph needs evidence")
            for ref in refs:
                item = evidence.get(ref)
                if not item:
                    errors.append(f"unknown evidence {ref}")
                    continue
                if item["public_use"] != "allowed":
                    errors.append(f"evidence {ref} lacks allowed public use")
                if p["kind"] == "fact" and item["classification"] not in {"confirmed_fact", "synthetic"}:
                    errors.append(f"evidence {ref} cannot be promoted to fact")
                if p["kind"] == "observation" and item["classification"] != "public_observation":
                    errors.append(f"evidence {ref} is not a public observation")
        for aid in page["asset_ids"]:
            item = assets.get(aid)
            if not item:
                errors.append(f"unknown asset {aid}")
                continue
            if item["public_use"] != "allowed":
                errors.append(f"asset {aid} lacks allowed public use")
            try:
                asset_file(item, root)
            except (OSError, ValueError, ET.ParseError) as exc:
                errors.append(f"asset {aid}: {exc}")
    return errors


def e(value):
    return html.escape(str(value), quote=True)


def render(data, root, kind):
    errors = validate(data, root, kind)
    if errors:
        raise ValueError("; ".join(errors))
    brand = data["brand"]
    pages = data[kind]["pages"]
    assets = {x["id"]: x for x in data["assets"]}
    label = "SYNTHETIC EXAMPLE / NOT A CLIENT RESULT" if data["is_synthetic"] else "REVIEW PROOF / NOT RELEASED"
    palette = brand["palette"]
    css = """*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.8 system-ui,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif}h1,h2,h3,p{margin:0}a{color:inherit;text-underline-offset:4px}.status{background:var(--ink);color:white;padding:9px 5vw;font:11px/1.7 system-ui;letter-spacing:.09em}.masthead{padding:22px 5vw;display:flex;justify-content:space-between;gap:30px;align-items:center;border-bottom:1px solid #ccc}.masthead strong{font:24px Georgia,serif}.masthead nav{display:flex;gap:20px;flex-wrap:wrap;font-size:13px}.masthead a{text-decoration:none}main{max-width:1180px;margin:auto}section{padding:70px 5vw;border-bottom:1px solid #ccc;scroll-margin-top:20px}h1{font-size:clamp(40px,5.8vw,76px);line-height:1.12;letter-spacing:-.04em;max-width:800px}h2{font-size:clamp(30px,3.9vw,47px);line-height:1.2;letter-spacing:-.025em}.kicker{font-size:11px;letter-spacing:.13em;text-transform:uppercase;margin-bottom:22px;color:var(--accent)}.standfirst{font-size:22px;line-height:1.65;margin:23px 0;max-width:740px}.copy{max-width:740px}.copy p{margin:18px 0}.copy sup{font-size:10px;margin-left:6px}.placeholder{border-left:2px solid var(--accent);padding-left:16px;font-style:italic}.editorial{color:#554f49}.observation::before{content:'Observation: ';font-size:11px;text-transform:uppercase}figure{margin:28px 0 0}figure img{display:block;width:100%;max-height:420px;object-fit:contain;background:#e6ddd1}figcaption{font-size:11px;margin-top:7px;color:#655e56}details{font-size:12px;line-height:1.8;margin:25px 0}details li{margin:10px 0;overflow-wrap:anywhere}.contact{background:var(--ink);color:white}.contact p{max-width:760px}footer{padding:24px 5vw;font-size:11px}.paper{position:relative;background:var(--paper);width:var(--trim-w);min-height:var(--trim-h);padding:14mm;margin:22px auto;border:1px solid #ccc;break-after:page}.paper h1{font-size:52px}.paper h2{font-size:36px}.paper .standfirst{font-size:19px}.paper .copy{font-size:15px;line-height:1.75}.paper figure img{max-height:95mm}.folio{margin-top:25px;padding-top:12px;border-top:1px solid #ccc;font-size:10px;display:flex;justify-content:space-between;gap:15px}.contents{font-size:13px;padding-left:20px}.contents li{margin:9px 0}.publication main{max-width:none}.publication .masthead{max-width:var(--trim-w);margin:auto}.cover{background:var(--accent);color:white}.cover .kicker,.cover .editorial,.cover figcaption{color:white}.cover figure img{background:transparent}.proof-note{font-size:12px;padding:20px;max-width:var(--trim-w);margin:auto}@media(max-width:760px){.masthead{align-items:flex-start;flex-direction:column;padding:20px}.masthead nav{gap:12px}section{padding:45px 20px}.standfirst{font-size:19px}.paper{width:100%;min-height:0;padding:28px 22px;margin:14px auto;border-left:0;border-right:0}.paper h1{font-size:43px}.paper h2{font-size:30px}.paper .copy{font-size:16px}.folio{margin-top:28px}}@media print{body{background:white}.masthead,.status,.proof-note{display:none}.paper{width:var(--trim-w);min-height:var(--trim-h);margin:0;border:0;box-shadow:none;break-after:page}.paper:last-child{break-after:auto}a{color:inherit}figure,figcaption{break-inside:avoid}}"""
    trim = data.get("publication", {})
    variables = f":root{{--ink:{palette['ink']};--paper:{palette['paper']};--accent:{palette['accent']};--trim-w:{trim.get('trim_width_mm',210)}mm;--trim-h:{trim.get('trim_height_mm',285)}mm}}"
    if kind == "publication":
        css += f"@page{{size:{trim['trim_width_mm']}mm {trim['trim_height_mm']}mm;margin:0}}"
    nav = "".join(f'<a href="#{e(p["id"])}">{e(p["headline"])}</a>' for p in pages)
    content = []
    for index, page in enumerate(pages, 1):
        tag = "h1" if index == 1 else "h2"
        cls = "paper " + page["role"] if kind == "publication" else "web-section"
        part = f'<section class="{e(cls)}" id="{e(page["id"])}"><p class="kicker">{e(label)} / {index:02d}</p><{tag}>{e(page["headline"])}</{tag}><p class="standfirst">{e(page["standfirst"])}</p>'
        if page["role"] == "contents" and kind == "publication":
            part += '<ol class="contents">' + "".join(f'<li><a href="#{e(p["id"])}">{i:02d} / {e(p["headline"])}</a></li>' for i, p in enumerate(pages, 1)) + '</ol>'
        part += '<div class="copy">'
        for paragraph in page["paragraphs"]:
            refs = ", ".join(e(x) for x in paragraph["evidence_ids"])
            part += f'<p class="{paragraph["kind"]}">{e(paragraph["text"])}' + (f'<sup>[{refs}]</sup>' if refs else "") + '</p>'
        part += '</div>'
        for aid in page["asset_ids"]:
            record = assets[aid]
            _, mime, raw = asset_file(record, root)
            src = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
            part += f'<figure><img src="{src}" alt="{e(record["alt"])}"><figcaption>{e(record["credit"])} / {e(record["permission_ref"])}</figcaption></figure>'
        if kind == "publication":
            part += f'<div class="folio"><span>{e(data["publication"]["title"])} / {e(data["publication"]["issue_label"])}</span><span>{index:02d} / {len(pages):02d}</span></div>'
        content.append(part + '</section>')
    sources = '<details><summary>Sources, rights and review / 来源与审核</summary><ul>'
    for item in data["evidence"]:
        # Unused restricted records must not leak through the audit appendix.
        used = any(item["id"] in p["evidence_ids"] for page in pages for p in page["paragraphs"])
        if used:
            sources += f'<li>{e(item["id"])} / {e(item["classification"])} / {e(item["statement"])} / {e(item["source_ref"])} / {e(item["as_of"])}</li>'
    sources += f'</ul><p>Content review: {e(data["review"]["content_status"])}. Public release: not granted. Structural checks do not verify truth, ownership or legal clearance.</p></details>'
    if kind == "website":
        tail = '<section class="contact" id="review-contact"><h2>Contact channel not connected</h2><p>This is a local review proof. It has no submission form, bookings, analytics, account access or publishing.</p></section>'
    else:
        tail = '<p class="proof-note">Screen/editorial proof only. Print CSS is not preflight: verify pagination, trim, bleed, image resolution, color, fonts and printer requirements before production.</p>'
    title = brand["name"] if kind == "website" else data["publication"]["title"]
    return f'<!doctype html><html lang="{e(brand["language"])}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>{e(title)} / review proof</title><style>{variables}{css}</style></head><body class="{kind}"><div class="status">{e(label)} / NO EXTERNAL ACTION PERFORMED</div><header class="masthead"><strong>{e(brand["name"])}</strong><nav aria-label="Sections">{nav}</nav></header><main>{"".join(content)}{tail}<section>{sources}</section></main><footer>Review proof, not released. Noindex is not access control; use private hosting when a preview needs restricted access.</footer></body></html>'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", type=Path, required=True)
    parser.add_argument("--kind", choices=["website", "publication"], required=True)
    parser.add_argument("--asset-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.brief.read_text(encoding="utf-8"))
        root = args.asset_root or args.brief.parent
        output = render(data, root, args.kind)
        if args.check_only:
            print(f"PASS {args.kind} production brief")
            return 0
        if not args.output:
            raise ValueError("--output is required unless --check-only is used")
        destination = args.output.resolve()
        sources = {args.brief.resolve()}
        sources.update((root / x["path"]).resolve() for x in data["assets"])
        if destination in sources:
            raise ValueError("output must not overwrite the brief or a registered source asset")
        if destination.exists() and not args.overwrite:
            raise ValueError("output exists; choose a new path or explicitly use --overwrite")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"PASS {args.kind} review proof: {args.output}")
        return 0
    except (OSError, ValueError, ET.ParseError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
