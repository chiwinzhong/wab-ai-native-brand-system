#!/usr/bin/env python3
"""Run positive and negative contract tests for WAB assessments."""

import copy
import json
import sys
from pathlib import Path

from validate_assessment import validate


def expect_valid(name, data):
    errors = validate(data)
    if errors:
        raise AssertionError(f"{name} should pass, got: {errors}")
    print(f"PASS valid: {name}")


def expect_invalid(name, data, expected_fragment):
    errors = validate(data)
    if not errors:
        raise AssertionError(f"{name} should fail")
    if not any(expected_fragment in error for error in errors):
        raise AssertionError(
            f"{name} failed for the wrong reason: expected {expected_fragment!r}, got {errors}"
        )
    print(f"PASS rejected: {name}")


def main():
    if len(sys.argv) != 2:
        print("Usage: run_contract_tests.py path/to/valid-assessment.json")
        raise SystemExit(2)

    fixture = Path(sys.argv[1])
    data = json.loads(fixture.read_text(encoding="utf-8"))
    expect_valid("reference assessment", data)

    unknown_evidence = copy.deepcopy(data)
    unknown_evidence["primary_bottleneck"]["evidence_ids"] = ["E99"]
    expect_invalid("unknown evidence reference", unknown_evidence, "unknown evidence ID E99")

    out_of_range_score = copy.deepcopy(data)
    out_of_range_score["lens_scores"]["proof_and_credibility"]["score"] = 4
    expect_invalid("out-of-range score", out_of_range_score, "integer from 0 to 3")

    missing_human_decision = copy.deepcopy(data)
    missing_human_decision["next_30_days"]["human_decisions"] = []
    expect_invalid("missing human decision", missing_human_decision, "human decision")

    unsafe_automation = copy.deepcopy(data)
    unsafe_automation["next_30_days"]["do_not_automate"] = []
    expect_invalid("missing automation boundary", unsafe_automation, "do-not-automate")

    print("All contract tests passed: 1 accepted, 4 correctly rejected.")


if __name__ == "__main__":
    main()
