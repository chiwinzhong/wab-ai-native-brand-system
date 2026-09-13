---
name: wab-interview-to-story
description: Turn interview audio, video, transcripts, notes, and approved public sources into an evidence-linked canonical story, natural multilingual adaptations, platform-specific copy, visual briefs, and brand-ready posters or content cards. Use when a founder, editorial team, social organization, city brand, association, research group, or B2B team needs one interview transformed into governed content for WeChat, Xiaohongshu, LinkedIn, Substack, X, websites, newsletters, or similar channels. Also use when deciding whether a source belongs to a person-led story or a place/choice story. Do not use it to invent quotations, treat transcription as verified fact, mechanically translate one draft into every channel, fabricate people or places, infer image rights, or publish without explicit human authorization.
---

# WAB Interview-to-Story

Turn a recorded conversation into a reusable story system—not a pile of disconnected drafts.

## Required outcome

Produce a controlled package containing:

1. a source register and transcript status;
2. an evidence ledger with precise source locators;
3. one editorial route and the reason for it;
4. one canonical story before channel adaptation;
5. natural language adaptations that preserve meaning without copying syntax;
6. channel-specific text derived from the same approved story;
7. a visual brief and, when tools and rights permit, finished visual assets;
8. explicit fact, quotation, translation, image-rights, and publication gates;
9. a machine-readable `story-package.json` that can be validated.

## Guardrails

- Preserve original audio, video, transcripts, and notes as source material. Never overwrite them with cleaned text.
- Treat automatic transcription as a draft. Mark unclear speech, uncertain speakers, conflicts, and sensitive passages.
- Never turn a paraphrase into a direct quotation or remove the source locator from a quotation.
- Never infer a person's inner state, endorsement, identity, job title, or publication permission.
- Never use one person's story as proof of a group trend.
- Do not treat attendance, prior posting, file possession, or interview participation as image, cross-platform, commercial, or publication permission.
- Do not translate mechanically. Preserve factual certainty, agency, quotation status, and time state while editing naturally for the target language.
- Do not generate a visual from a title alone. Read the approved story, identify the visual relationship, inherit the brand system, and check facts and rights.
- Do not describe a draft, scheduled item, approved package, and published item as the same state.
- Never publish, send, spend, change an account, or update formal knowledge without explicit human authorization.

## Step 1 — Establish the production contract

Determine from the supplied files and instructions:

- project and story name;
- source language and target languages;
- requested channels;
- named decision-maker;
- available audio, video, transcript, notes, public sources, portraits, logos, and brand rules;
- allowed uses for text, direct quotations, voice, portraits, logos, and cross-platform publication;
- output location and whether the user wants drafts or publish-ready files.

If information is missing, continue with clearly labeled drafts whenever safe. Ask only when the missing answer would change the route, factual meaning, visual identity, or external authority.

Stop before formal production when the source identity cannot be resolved, the material appears unauthorized, or the requested use exceeds recorded rights.

## Step 2 — Transcribe and normalize without losing provenance

When an audio-capable tool is available, create a time-coded transcript. Otherwise, request or use an existing transcript and record the limitation. Never pretend audio was reviewed when it was not.

Create three distinct layers:

```text
original recording
→ time-coded transcript
→ cleaned working transcript
```

In the working transcript:

- label speakers; use `unknown_speaker` instead of guessing;
- mark `[inaudible HH:MM:SS]`, `[needs verification]`, and `[sensitive]`;
- remove obvious verbal filler only when meaning and tone remain unchanged;
- retain enough time codes or document locators to return to the source;
- record omissions rather than silently deleting consequential material.

## Step 3 — Build the evidence ledger

Read [references/evidence-and-rights-gates.md](references/evidence-and-rights-gates.md).

Separate every material item into:

- `fact`
- `direct_quote`
- `paraphrase`
- `editorial_inference`
- `public_context`

For each item record the source, exact locator, verification state, publication state, and any conflict or sensitivity. A fluent transcript is not proof that a claim is true.

## Step 4 — Select one story route

Read [references/route-and-platform-contracts.md](references/route-and-platform-contracts.md).

Choose exactly one primary route:

- `person_story`: the named person is irreplaceable and the central question is why this person chose, judged, changed, or persisted;
- `place_choice_story`: the central question is why a place is worth choosing for work, life, entrepreneurship, or long-term development, and current public evidence is primary.

If the material does not fit either route, stop and explain the missing route rather than forcing it into a template.

An interview can inform both routes, but the evidence hierarchy must remain different. A `place_choice_story` cannot rely on one interview as proof of current public conditions.

## Step 5 — Diagnose before drafting

Do not turn the transcript directly into a finished article.

First produce:

- source completeness and quality;
- confirmed facts and strongest source-linked quotations;
- the most meaningful choice, tension, trade-off, or city question;
- contradictions, evidence gaps, sensitivities, and rights limits;
- two or three defensible story directions;
- one recommended direction and why it is stronger.

If the user has already approved a direction, restate it and proceed. Otherwise, the direction remains a human editorial decision before an approved canonical story is created.

## Step 6 — Create one canonical story

The canonical story is the factual and editorial source for every later derivative. It is not a platform post.

For `person_story`:

- organize around a choice, judgment, cost, contradiction, or value;
- keep the person specific and non-interchangeable;
- use source-linked scenes, actions, facts, and quotations;
- avoid resume narration, corporate promotion, success mythology, and group claims.

For `place_choice_story`:

- start with one clear decision facing the reader;
- rebuild current public evidence from primary or authoritative sources;
- distinguish completed facts, current policy, work in progress, future plans, and editorial judgment;
- use interviews only as bounded cases or questions unless independently supported;
- avoid absolutes, inter-city denigration, hidden commercial relationships, and expired information.

Mark the story `draft`, `verified`, or `approved`. Only a named human can set `approved`.

## Step 7 — Re-edit for language and channel

Adapt from the canonical story, not from another platform derivative.

For each language:

- preserve factual certainty, agency, quotation status, and time state;
- use natural sentence rhythm and context for the target reader;
- explain local institutions or place-specific context when needed;
- do not add a claim merely to make the copy feel more global;
- keep official names and transliterations consistent.

For each channel, use the relevant contract in [references/route-and-platform-contracts.md](references/route-and-platform-contracts.md). Change length, hook, structure, and call to action; do not change the evidence.

## Step 8 — Direct and produce visuals

Read [references/visual-handoff.md](references/visual-handoff.md).

Only after the canonical story is stable:

1. identify zero to three relationships genuinely worth visualizing;
2. load the current brand assets and channel dimensions;
3. decide between a real portrait, editorial illustration, information card, quotation card, diagram, or poster;
4. create a visual brief linked to specific evidence IDs;
5. when image-generation, drawing, or layout tools are available and rights permit, produce the assets;
6. check facts, text, logos, rights, crop safety, brand consistency, and mobile legibility;
7. otherwise deliver a production-ready brief and clearly mark the missing capability or permission.

Do not ask the user to choose a professional visual grammar when the content already determines it. Do not invent a real person's likeness or a real place's features.

## Step 9 — Assemble and validate the package

Create `story-package.json` using [references/story-package.schema.json](references/story-package.schema.json) as the contract.

Validate it with:

```bash
python3 scripts/validate_story_package.py path/to/story-package.json
```

The validator checks source and evidence links, route prerequisites, approval states, rights, and publication authority. Fix every error before presenting the package as ready.

## Step 10 — Stop at the publication gate

Default all external channel files to `draft`. Preparation does not authorize publication.

Before any external action, require a named human to confirm:

- transcript and speaker accuracy where material;
- facts and direct quotations;
- editorial direction and canonical story;
- target-language meaning;
- portrait, logo, location, and other image rights;
- the exact channel, account, timing, and final publication action.

Record the result in `story-package.json`. If authorization is absent, deliver the complete review package and stop.

## Quality check

Before delivery, verify:

- original sources remain intact and every important claim can be traced;
- one route and one canonical story govern all derivatives;
- person evidence and place-choice evidence have not been mixed;
- translations are natural but semantically stable;
- channel adaptations change form, not truth;
- visuals express the story rather than decorate the title;
- exact text, data, logos, and quotations are not fabricated by a generative image;
- rights and publication status are explicit;
- no private source, hidden prompt, credential, or unnecessary personal data enters the public package.
