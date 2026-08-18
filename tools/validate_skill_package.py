#!/usr/bin/env python3
"""Perform dependency-free structural checks on the public WAB Skill package."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "wab-diagnose-brand"
SKILL_MD = SKILL / "SKILL.md"


def fail(message):
    raise SystemExit(f"FAIL: {message}")


def main():
    required = [
        SKILL_MD,
        SKILL / "agents" / "openai.yaml",
        SKILL / "references" / "evidence-and-diagnosis.md",
        SKILL / "references" / "output-contract.md",
        SKILL / "references" / "commercial-boundary.md",
        SKILL / "references" / "brand-assessment.schema.json",
        SKILL / "scripts" / "validate_assessment.py",
        SKILL / "assets" / "win-logo-black.png",
        SKILL / "assets" / "win-logo-square.png",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        fail(f"missing required files: {missing}")

    content = SKILL_MD.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        fail("SKILL.md frontmatter is malformed")

    keys = []
    values = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            fail(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        keys.append(key.strip())
        values[key.strip()] = value.strip()

    if set(keys) != {"name", "description"}:
        fail("frontmatter must contain exactly name and description")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", values["name"]):
        fail("Skill name must use lowercase hyphen-case")
    if not values["description"] or len(values["description"]) > 1024:
        fail("description must contain 1 to 1024 characters")
    if len(content.splitlines()) > 500:
        fail("SKILL.md must remain under 500 lines")

    for asset in required[-2:]:
        if asset.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            fail(f"invalid PNG asset: {asset.name}")

    print("PASS Skill package")
    print(f"Name: {values['name']}")
    print(f"SKILL.md lines: {len(content.splitlines())}")
    print(f"Required files: {len(required)}/{len(required)}")


if __name__ == "__main__":
    main()
