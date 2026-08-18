# Evidence and diagnosis model

Use this reference to classify evidence and score brand readiness. Do not use it as a substitute for the user's business context.

## Evidence types

| Type | Meaning | Typical source | Allowed use |
| --- | --- | --- | --- |
| `confirmed_fact` | Confirmed by an authorized owner or primary record | contract, product record, approved document | May support factual statements within its scope |
| `public_observation` | Directly visible on a public page | official site, account, product page | May describe what the market can currently see |
| `management_claim` | Statement from a founder or manager not yet independently confirmed | interview, questionnaire | May frame hypotheses and verification questions |
| `customer_signal` | Observable customer behavior or feedback with provenance | review, inquiry log, interview | May support audience or choice-barrier analysis |
| `agent_hypothesis` | Interpretation generated from available inputs | assessment | Must remain falsifiable and labeled |
| `conflict` | Two credible inputs disagree | public page vs approved internal record | Must be escalated; never silently resolved |
| `gap` | Material information is missing | absent proof, unknown owner, unavailable source | Must reduce confidence and shape the next action |

## Evidence strength

- `strong`: primary, current, directly relevant, and attributable;
- `medium`: relevant but indirect, incomplete, or awaiting confirmation;
- `weak`: anecdotal, old, ambiguous, or based on a single unverified signal.

## Six readiness lenses

### 1. Position and difference

Determine whether the brand can state who it is for, what problem it solves, and why it should be chosen over a realistic alternative.

### 2. Audience and choice barrier

Determine whether the priority audience, decision context, current barrier, and desired next action are specific enough to guide work.

### 3. Proof and credibility

Determine whether the brand has product facts, operating evidence, cases, customer signals, credentials, or other proof proportionate to its claims.

### 4. Experience and consistency

Determine whether the market receives a coherent promise across content, sales, product, service, and visual touchpoints.

### 5. Knowledge and workflow

Determine whether facts, decisions, templates, permissions, owners, review gates, and change history are reusable beyond one individual.

### 6. Commercial signal and learning

Determine whether the organization distinguishes output, reach, engagement, inquiry, payment, retention, and repeatable result—and feeds valid learning back into decisions.

## Scoring rubric

- `0 — unknown`: insufficient evidence to judge;
- `1 — weak`: mostly claims, isolated activity, or person-dependent execution;
- `2 — partial`: some evidence and repeatability, but important gaps or conflicts remain;
- `3 — supported`: current evidence, clear ownership, and repeatable execution support the decision.

Do not calculate a total score. A high score in content production cannot compensate for a weak position or unsupported proof.

## Four differentiation gates

1. `true`: What current evidence makes this more than a slogan?
2. `relevant`: Why does the priority audience care in this decision?
3. `ownable`: How is this different from realistic alternatives, including doing nothing or using generic AI?
4. `deliverable`: What operating capability allows the organization to keep the promise?

Return `pass`, `partial`, or `fail` for each gate and cite evidence IDs or gaps.
