# Synthetic Interview-to-Story example

This package is fictional. It demonstrates the machine-readable contract without exposing a real recording, interviewee, organization, or unpublished story.

The example stops before publication: its source-language canonical story is approved, while channel drafts and visuals remain under review.

Validate it with:

```bash
python3 skills/wab-interview-to-story/scripts/validate_story_package.py \
  examples/interview-to-story/story-package.json
```

Run positive and negative contract tests with:

```bash
python3 skills/wab-interview-to-story/scripts/run_contract_tests.py \
  examples/interview-to-story/story-package.json
```
