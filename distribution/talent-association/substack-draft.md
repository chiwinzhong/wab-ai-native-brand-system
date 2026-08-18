# An Interview Is Not a Content Package

*A field note from China on turning recorded human judgment into multilingual stories and visual assets without losing the evidence behind them.*

> Draft only. Not authorized for publication.

An interview can now be transcribed in minutes.

That is useful. It is also the least interesting part of the problem.

The harder question is what happens next.

How do you turn a two-hour conversation into a story without converting every fluent sentence into a fact? How do you preserve a person's actual judgment instead of flattening the interview into a resume? How do you create Chinese and English editions without allowing the English version to become more promotional than the source? How do you produce a LinkedIn post, a Substack article, an X thread, a WeChat story, and a poster without letting five versions of the truth emerge?

This is the problem behind a new public Skill I am developing: **WAB Interview-to-Story**.

## A transcript is evidence, not an article

The public field case comes from only two editorial series developed by 东莞市人才资源发展促进会: 《即莞来》 and 《选择东莞》.

I am deliberately not publishing the association's wider operating system. These two routes are enough to show the core capability.

The production chain looks like this:

```text
interview audio or notes
→ time-coded transcript
→ cleaned working transcript
→ evidence ledger
→ story-route decision
→ editorial diagnosis
→ approved canonical story
→ Chinese channel adaptations
→ natural English re-edit
→ international channel adaptations
→ visual brief
→ cards, covers, or posters
→ human publication decision
```

Each arrow contains a decision that a transcription tool does not make safely by itself.

Automatic transcription can misidentify speakers, punctuation, names, dates, and technical terms. Even a perfect transcript does not tell an editor what matters, which claim needs verification, which sentence is a direct quotation, which passage is sensitive, or which story the material can honestly support.

So the Skill preserves three separate layers: the original recording, a time-coded transcript, and a cleaned working transcript. Important facts and quotations keep exact source locators. Unclear speech remains unclear. Conflicting sources remain in conflict. A paraphrase never becomes a quotation because it sounds better inside a headline.

That provenance is not bureaucracy added after writing. It is what makes later reuse possible.

## Two interviews can require different truth systems

The two series use different editorial routes.

In 《即莞来》, the person is irreplaceable. The story asks what this person chose, how they judged the situation, what the choice cost, and what their experience reveals about a real relationship with Dongguan, an industry, or a changing time.

The interview is the primary evidence. But the transcript is not rewritten in sequence. The editor first separates facts, quotations, paraphrases, interpretation, conflicts, and sensitive content. Then the system proposes two or three defensible story directions. Only after a human confirms the direction does it build the canonical story.

This prevents a common AI failure: turning a life into a polished corporate profile simply because job titles and achievements are easy to summarize.

In 《选择东莞》, the person may reveal the question, but the article has a different responsibility. It asks what a reader should understand before choosing Dongguan for work, entrepreneurship, life, or long-term development.

One interview cannot establish current city conditions. The primary evidence must come from current official or authoritative public sources. A policy has an effective period. A planned project is not a completed result. One person's positive experience is not a guarantee for everyone.

This route can be optimistic. It cannot be careless.

The distinction matters beyond Dongguan. Many organizations mix personal stories, place branding, public information, and institutional promotion in one content workflow. The same source then gets reshaped until its original evidentiary status disappears.

Routing is how the Skill protects the story before generation begins.

## One canonical story before many platforms

Most repurposing tools begin with a finished post and ask how many other posts they can derive from it.

WAB Interview-to-Story begins one layer earlier.

It creates an approved canonical story tied to an evidence ledger. Every platform derivative returns to that source.

The WeChat edition may carry the complete Chinese editorial experience. A LinkedIn post may lead with one professional insight. A Substack article may expand the mechanism and field limitation. An X thread may separate the argument into one claim per post. A poster may express one verified quotation or one visual relationship.

These outputs should not have identical words. They should have identical truth conditions.

The same rule applies to English.

Natural English is not literal English. A good English editor may split a long Chinese sentence, change paragraph rhythm, add necessary context, or choose a more natural verb. But four things must remain stable: factual certainty, who acted, whether a sentence is a quotation, and whether an event happened, is happening, or is only planned.

Localization changes how the story travels. It must not change what the story can prove.

## The poster is also an evidence product

Visual production creates another form of drift.

A model can generate an attractive person, skyline, factory, meeting, or policy scene. That does not make the scene true.

The Skill therefore starts visual work only after the canonical story is stable. It identifies what is genuinely worth visualizing: a defining choice, a verified quotation, a before-and-after relationship, a place-choice mechanism, or a small evidence-backed set of facts.

It then decides whether the appropriate form is a portrait card, quotation card, editorial illustration, explainer, cover, or poster.

Real portraits, supplied photographs, logos, recognizable places, and exact quotations have separate source and rights records. Generative imagery can create an editorial illustration or visual background. Exact Chinese text, names, dates, figures, logos, and data are better handled with controlled layout.

This distinction sounds technical. It is really about editorial honesty.

## What is now open

The public repository includes:

- the Agent Skill;
- evidence and rights gates;
- the person and place/choice routes;
- domestic and international platform contracts;
- the visual handoff contract;
- a machine-readable story-package schema;
- a dependency-free validator;
- negative contract tests;
- a fictional sample package.

The validator rejects several dangerous states. A person story cannot pass without a transcript or interview notes. A place/choice story cannot pass without a current public source. An approved output cannot depend on pending or blocked evidence. A published item cannot exist without final publication approval.

This does not make the Skill an autonomous publisher. It makes the stopping points inspectable.

## The claim I can make today

Here is the bounded claim:

> Two recurring editorial patterns have been converted into an inspectable Skill that can transform interview material into source-linked, multilingual, channel-specific story and visual packages while retaining explicit human gates.

I am not yet claiming that the Skill improves reach, conversion, trust, or efficiency. I am not claiming that automatic transcription removes editorial review. I am not claiming that one organization's route transfers unchanged to another.

Those claims require evidence that can be reviewed without exposing the people behind the interviews.

## The next test

The next public proof should include one package for each route:

1. a redacted source excerpt or synthetic equivalent;
2. the evidence ledger;
3. the route decision;
4. the canonical story;
5. one Chinese and one English platform adaptation;
6. one reviewed visual asset;
7. the human corrections and failure log.

I also want to compare the Skill with a prompt-only baseline using the same source material, model, channels, and time budget. The useful measures are not only speed. They include unsupported claims, quotation drift, source traceability, human corrections, cross-channel contradictions, and visual rework.

The open Skill and exploratory case are prepared in the WAB repository:

`https://github.com/chiwinzhong/wab-ai-native-brand-system`

The commercial idea is simple:

> One interview can become many assets. One approved truth should remain behind all of them.

Where does this model overclaim—and which part would you test first?
