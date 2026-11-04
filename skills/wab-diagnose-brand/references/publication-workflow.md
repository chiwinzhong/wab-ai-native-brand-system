# Magazine and publication workflow / 杂志、内刊与企业刊物

Use this for an editorial issue, internal journal, brand magazine, annual publication or booklet. Preserve the user's medium and purpose; a magazine is not a long website printed into arbitrary equal pages.

## Inputs

Establish audience and reading occasion; issue theme and date; digital, internal or public/paid distribution; target language; editorial owner; brand/visual rules; intended page count or budget; trim, binding and printer specification when applicable. Read supplied manuscripts in full, retaining bylines, headings, quotes, captions and source locations. If a claimed original manuscript is missing, identify that gap and label any newly written draft rather than saying the original was typeset.

Obtain only the necessary article facts, interviews, product information, illustrations/photos, credits and permissions. Record whether a source permits internal review, public display, print, redistribution or adaptation. A photographer credit is not a license. A public social post is not automatic permission to reproduce it in a magazine. Do not upload the publisher's internal archive into a public Skill.

## Editorial and layout sequence

1. **Set one issue proposition.** Define what the reader should understand or do after reading. Group the material into cover promise, contents/editorial, features, shorter sections and colophon/credits as appropriate. Keep proposed claims separate from established facts.
2. **Make a page plan.** For each page/spread record role, article, approximate word budget, hierarchy, image, source/right IDs, caption, byline, and reviewer. Allocate space according to reading rhythm, not a fixed equal word count. Determine whether the first page stands alone, where spreads fall, and whether total pages/signatures suit the actual printer and binding; do not force multiples of four for every digital or binding method.
3. **Edit before polishing layout.** Resolve duplicated passages, transitions, headline promises, quotations, names, dates, units, product details and claims. Track substantive edits. Do not silently invent quotes, interview answers, circulation, issue numbers, ISSNs, publication approvals, awards or business results.
4. **Build a visual system.** Carry the authorized brand identity into grids, heading/body/caption hierarchy, folios, recurring section markers and image treatments. Keep body text readable. Never deform a logo, fabricate Chinese lettering, remove source watermarks or alter a product's material features to make the page look consistent.
5. **Produce the reader proof.** Render a coherent cover, contents, features and closing/credits using the actual layout tools available. Show facing pages when reviewing spread relationships. Keep web, screen PDF and print production as distinct targets. The bundled HTML helper is a proof, not a substitute for a tested native layout file.
6. **Review every rendered page.** Check overflow, missing glyphs, widows/orphans where relevant, running heads, folios, contents/page references, image crop, captions, bylines, links and reading order. Recheck the latest render after changes; text extraction cannot prove visual quality. Preserve source and version references.
7. **Prepare the appropriate outputs.** Digital: searchable/readable PDF or an actual tested web reader, links, alt text/accessibility notes and optimized images. Print: native production source plus the printer-agreed PDF, trim/bleed, color profile, effective image resolution, font embedding/license and finishing notes. Do not call a browser print or a screen PDF "press-ready" without the agreed preflight and sign-off.
8. **Approve release and record learning.** Named editor confirms facts/quotes; rights owner clears material; designer/production reviewer clears the latest proof; authorized publisher decides distribution. Check applicable publication/distribution requirements with the responsible human reviewer. A mockup is not a registered periodical or an approved public issue. Record corrections and approved reusable rules without auto-writing official knowledge.

## Minimum handoff

- issue proposition, audience, medium and editorial owner;
- complete article/page map, source ledger, byline and asset-rights inventory;
- review proof, editable source and actual exports;
- page-level QA and unresolved items;
- credits/colophon, version and explicit distribution status;
- printer handoff/preflight if print is in scope, otherwise a clear screen-proof limitation.

## Bundled proof helper

`scripts/render_brand_deliverable.py --kind publication` renders the brief's ordered pages as standalone HTML with a contents map, folios, captions and print CSS for the chosen trim. On small screens it allows each page to flow for reading. It does not verify print pagination, bleed marks, CMYK, image DPI, PDF accessibility or font embedding; these remain production checks in the actual export workflow.

The fictional `magazine-cover-reference.png` and `magazine-spread-reference.png` illustrate a cover/feature hierarchy. Read `assets/production/rights.json`; do not present them as a real published magazine or customer case.
