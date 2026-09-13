#!/usr/bin/env python3
"""Perform dependency-free structural checks on the public WAB Skill packages."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "wab-diagnose-brand": [
        "SKILL.md",
        "agents/openai.yaml",
        "references/evidence-and-diagnosis.md",
        "references/output-contract.md",
        "references/commercial-boundary.md",
        "references/brand-assessment.schema.json",
        "scripts/validate_assessment.py",
        "scripts/run_contract_tests.py",
        "assets/win-logo-black.png",
        "assets/win-logo-square.png",
    ],
    "wab-interview-to-story": [
        "SKILL.md",
        "agents/openai.yaml",
        "references/evidence-and-rights-gates.md",
        "references/route-and-platform-contracts.md",
        "references/visual-handoff.md",
        "references/story-package.schema.json",
        "scripts/validate_story_package.py",
        "scripts/run_contract_tests.py",
        "assets/story-package-template.json",
        "assets/win-logo-black.png",
        "assets/win-logo-square.png",
    ],
}


def fail(message):
    raise SystemExit(f"FAIL: {message}")


def validate_skill(name, relative_files):
    skill = ROOT / "skills" / name
    required = [skill / path for path in relative_files]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        fail(f"{name} missing required files: {missing}")

    skill_md = skill / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        fail(f"{name} SKILL.md must start with YAML frontmatter")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        fail(f"{name} SKILL.md frontmatter is malformed")

    keys = []
    values = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            fail(f"{name} invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        keys.append(key.strip())
        values[key.strip()] = value.strip()

    if set(keys) != {"name", "description"}:
        fail(f"{name} frontmatter must contain exactly name and description")
    if values["name"] != name:
        fail(f"{name} frontmatter name does not match directory")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", values["name"]):
        fail(f"{name} must use lowercase hyphen-case")
    if not values["description"] or len(values["description"]) > 1024:
        fail(f"{name} description must contain 1 to 1024 characters")
    if len(content.splitlines()) > 500:
        fail(f"{name} SKILL.md must remain under 500 lines")

    for relative in relative_files:
        if relative.endswith(".png"):
            asset = skill / relative
            if asset.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                fail(f"{name} has invalid PNG asset: {relative}")

    print(f"PASS {name}")
    print(f"SKILL.md lines: {len(content.splitlines())}")
    print(f"Required files: {len(required)}/{len(required)}")


def main():
    for name, relative_files in SKILLS.items():
        validate_skill(name, relative_files)
    print(f"PASS all Skill packages: {len(SKILLS)}")


if __name__ == "__main__":
    main()
