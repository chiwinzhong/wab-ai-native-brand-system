# Production source and review contract

The public website/publication modes share one explicit brief, not an inferred client database. Use `production-brief.schema.json`; do not change the diagnosis assessment contract to hold layout pages.

## Records

- **Brand and objective:** one brand, primary audience, approved decision/brief reference, language and intended next action.
- **Evidence:** unique ID, statement, classification, exact source reference, as-of date and allowed public-use status. A source's publication date and access date are not interchangeable.
- **Assets:** unique ID, local path, alt text, author/credit, license/permission reference and allowed-use status. Internal review permission does not imply public redistribution.
- **Copy:** headline/standfirst plus paragraph records. `fact` paragraphs cite confirmed or explicitly synthetic evidence; `observation` paragraphs cite public observations and remain observations. `editorial` is proposed wording/judgment, not a shortcut for unsupported factual claims. `placeholder` carries no private assertion. Humans must check semantic support across every text field, including headlines and captions.
- **Website:** page/section purpose and desired next action. The bundled proof is a single-file website with section navigation.
- **Publication:** ordered page roles and issue metadata, trim and source/asset mappings. No implied registered issue status.
- **Review:** `draft` or `approved` content with reviewer/time/record when approved. Distribution authority is always a separate gate; helpers perform no external actions.

## Rules before rendering

Used facts and assets must have `public_use=allowed`, even in a draft intended for possible public review. Exclude pending/restricted material and render a neutral placeholder instead. Approved private-client workflows can keep restricted records in the client's own system, but must not feed them into these shareable public examples.

The renderer checks structure, references, allowed asset paths, basic SVG safety and explicit approval metadata. It escapes text and embeds local approved assets; it does not browse, prove truth, determine copyright ownership, inspect all image content, replace an editor or certify legal compliance. Review the actual rendered result and the substance of every source.

## Do not infer completion

Keep `content_review`, `preview`, `deployment`, `public_distribution`, `printing` and `knowledge_adoption` separate. Rendering a file does not satisfy the other states. Do not auto-publish, submit forms, purchase printing, accept terms, grant access or replace official sources. For an uncertain external operation, inspect its actual receipt/state before any retry.

## Portable use

The demo brief and its images live inside `assets/production/` so a copied Skill remains usable without the rest of this repository. Asset paths are relative to the brief directory, or an explicitly provided `--asset-root`; absolute paths, parent traversal, symlink escape and remote image URLs are rejected. The output must not overwrite the brief or any registered source asset, even with `--overwrite`.

The four layout-reference PNGs are original synthetic illustrations under this repository's Apache 2.0 license, with no WIN/WAB logo rights granted. They are not generated screenshots or independent performance evidence. Use the actual client's licensed identity rather than copying the demo style by default.
