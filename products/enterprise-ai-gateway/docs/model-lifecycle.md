# Model and policy lifecycle

**Implemented:** model state and review expiry constrain eligibility; use-case approval and review expiry constrain purpose. Signed policy site/revision/digest checks prevent ordinary local rollback. Generate requests are bound to policy and document context.

**Operating contract:** proposal → supplier review → evaluation → independent approval → canary → observation → retirement. Retain owner, version, intended/prohibited use, modalities, provenance, region/retention declaration, evaluation cohort, expiry and retirement trigger.

Changing a model, prompt, retrieval corpus, detector, provider API or routing rule may alter risk. Require new evidence for the affected use cases. Suspend a model without offering an ineligible alternative. Communicate retirement to application owners and preserve an exit path.

Rollback is a new governed change, not permission to ignore a revision watermark. A production recovery checkpoint must preserve trusted revision/digest independently of a restored store. No online policy administration or automated canary is implemented.
