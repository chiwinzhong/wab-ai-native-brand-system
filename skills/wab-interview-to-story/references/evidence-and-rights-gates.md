# Evidence and rights gates

## Evidence classes

| Class | Meaning | Minimum record |
| --- | --- | --- |
| `fact` | A claim about identity, time, place, action, role, result, or condition | source ID, locator, verification, publication state |
| `direct_quote` | Words represented as spoken or written by a named speaker | recording or document locator, speaker check, quotation check |
| `paraphrase` | A concise restatement faithful to the source | source locator; never use quotation marks |
| `editorial_inference` | The editor's interpretation of the material | label as inference; do not attribute to the speaker |
| `public_context` | Current external fact, policy, statistic, institution, or place context | original URL or authoritative file, date, scope, last verification |

## Verification states

- `confirmed`: checked against an adequate source for the intended use;
- `pending`: plausible but not ready for approved output;
- `conflict`: two or more sources disagree;
- `excluded`: intentionally withheld or unusable.

## Publication states

- `allowed`: item-level use is approved for the stated package;
- `draft_only`: the item may appear in internal drafts but not approved outputs;
- `blocked`: the item must not appear.

## Rights are not interchangeable

Record text, quotation, voice, portrait, supplied photograph, logo, cross-platform, commercial, archive, and model-training rights separately when relevant.

The following do not create broad permission:

- agreeing to an interview;
- appearing at an event;
- sending a photograph;
- membership or partnership;
- a previous post;
- public availability;
- possession of the file.

When the rights record is missing, keep the material in a private draft and use `unknown` rather than guessing.

## Required human gates

| Gate | Required before |
| --- | --- |
| transcript review | treating automatic transcription as the working record |
| fact and quotation review | marking the canonical story `verified` |
| direction approval | marking the canonical story `approved` |
| translation review | approving a target-language derivative |
| image-rights review | approving a portrait, supplied photo, logo, or location-dependent visual |
| final publication approval | setting any channel output to `published` or taking an external action |

Approval must identify the decision-maker, scope, date, and channels. Silence, scheduling, or completion of the package is not approval.

## Public-package privacy rule

Include only the minimum evidence necessary to explain and audit the public claim. Do not expose raw recordings, full transcripts, contact details, private correspondence, local filesystem paths, credentials, hidden prompts, or unpublished third-party material.
