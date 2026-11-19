# Human approval and delegated action record

**Synthetic example:** gov-app requests maintenance.schedule(asset-a, day); two independent reviewers; exact policy/action/requester/tenant digest; 120-second single-use grants. The action only creates a synthetic record.

For a real service show requester, delegated subject, tool identity, exact arguments, asset, destination, consequence, reversibility, business policy, reviewers, expiry and idempotency. The approval screen must display the actual reviewed parameters.

Parameter changes invalidate prior approval. The downstream service independently checks resource authority. Implement revocation of issued grants; reviewer credential revocation alone is insufficient in this reference.
