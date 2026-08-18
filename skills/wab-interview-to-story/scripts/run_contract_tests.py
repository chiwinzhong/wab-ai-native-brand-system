#!/usr/bin/env python3
"""Run positive and negative contract tests for WAB Interview-to-Story."""

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run(validator, payload, should_pass, label):
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        path = Path(handle.name)
    try:
        result = subprocess.run([sys.executable, str(validator), str(path)], capture_output=True, text=True)
    finally:
        path.unlink(missing_ok=True)
    passed = result.returncode == 0
    if passed != should_pass:
        print(f"FAIL: {label}")
        print(result.stdout or result.stderr)
        raise SystemExit(1)
    print(f"PASS: {label}")


def main():
    if len(sys.argv) != 2:
        print("Usage: run_contract_tests.py path/to/valid-story-package.json")
        raise SystemExit(2)
    sample_path = Path(sys.argv[1])
    sample = json.loads(sample_path.read_text(encoding="utf-8"))
    validator = Path(__file__).with_name("validate_story_package.py")

    run(validator, sample, True, "valid package")

    missing_transcript = copy.deepcopy(sample)
    for source in missing_transcript["source_register"]:
        if source["kind"] == "transcript":
            source["status"] = "missing"
    run(validator, missing_transcript, False, "person story without transcript or notes")

    premature_publication = copy.deepcopy(sample)
    premature_publication["deliverables"][0]["status"] = "published"
    run(validator, premature_publication, False, "publication without final approval")

    unverified_claim = copy.deepcopy(sample)
    unverified_claim["deliverables"][0]["status"] = "approved"
    unverified_claim["evidence_ledger"][0]["verification"] = "pending"
    run(validator, unverified_claim, False, "approved output with pending evidence")

    print("ALL CONTRACT TESTS PASSED")


if __name__ == "__main__":
    main()
