# Website production workflow / 品牌网站

Use this reference for a new site or a bounded change to an existing site. Reuse approved strategy; diagnose only the unresolved decision that materially affects the site.

## Input and scope

Read the current site/source, repository instructions, requested template, brand facts, approved identity assets, audience, desired next action, product/service scope, and source/rights register. Record the existing site identity, branch/version and access audience before editing. A screenshot is a visual reference, not a source-code license.

Ask only for a missing fact that changes the result. Without a supplied template, use a clearly labeled proposed design; never claim to have adapted a template that was not received. Without verified contact details, show an explicit unconnected state: do not invent email addresses, QR codes, clients, form submissions, or a "success" message.

## Work sequence

1. **Map content to sources.** Build a compact matrix: page, audience question, approved claim/evidence ID, asset/license, reviewer, gap. Distinguish confirmed facts, public observations, proposals and missing information. Apply [production-contract.md](production-contract.md).
2. **Design the visitor path.** Lead from the customer's problem to an appropriate service/product, substantiated proof and a real next action. Use home, solutions/products, evidence, about and contact when useful; do not create empty pages merely to meet a count. Exclude unauthorized cases rather than presenting them as anonymous proven success.
3. **Write and map to the template.** Define one page purpose, headline, supporting information, evidence and CTA. Preserve real names and approved product relationships. Replace all template sample metrics and testimonials. Maintain a shared content model while adapting the reading order to each page.
4. **Implement the actual experience.** Prefer the website tools already available in the target environment. Otherwise build portable HTML/CSS/JS, keeping content, assets and presentation separable. Match the chosen template; finish navigation, keyboard access, mobile menu, images and contact behavior. Do not claim a backend, booking integration, analytics or CMS that has not been connected and tested.
5. **Inspect a representative desktop and mobile width.** Check horizontal overflow, text wrapping, navigation, focus/contrast, image loading, alternative text, links, dialogs, anchor targets, and real CTA behavior. Exercise consequential paths with authorized test data only. Record dimensions, observed results and untested parts; do not describe static linting as browser testing.
6. **Package for review.** Deliver source, assets/rights register, content/source map, a working preview or portable file, and a short change summary. Check that an offline export really embeds its dependencies; HTTP success alone is not a device preview. Do not give an unpublished expected URL or a loopback URL on another host as a live site.
7. **Release only within current authority.** Preserve the existing audience, domain, repository and account. Public marketing, new access grants, paid hosting, form-data transmission, legal acceptance and domain changes require their own authority. Check the actual deployment result. After a timeout, inspect the existing version/deployment before retrying; never create a duplicate site as recovery.

## Minimum handoff

- visitor journey and page/section inventory;
- final draft copy with source and rights IDs;
- actual source and assets, including the supplied template's license boundary;
- preview URL/file and verification notes;
- real contact state, unresolved facts, reviewer and release status;
- maintenance entry: where content, versions, permissions and feedback belong.

Keep drafts and adopted company sources separate. A website revision does not silently change contracts, prices, a company knowledge base or other clients' materials.

## Bundled proof helper

`scripts/render_brand_deliverable.py --kind website` validates a production brief and creates a responsive, single-file section-based website proof with inline authorized assets. It is suitable for reviewing copy, hierarchy and source links. It does **not** implement multi-page hosting, authentication, data collection or publishing. Use the actual site's stack for those requirements.

See `assets/production/website-desktop-reference.png` and `website-mobile-reference.png` for fictional layout illustrations. They are references, not screenshots or templates that every brand must copy.
