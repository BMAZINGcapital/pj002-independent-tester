# PJ002 Independent Tester

Public, bounded independent-testing harness for PRIMAL JUNGLE 002.

## Authority boundary

This repository does **not** admit, deploy, govern, or authorize PJ002. It exists only to run a frozen test payload on a GitHub-hosted runner and produce an externally attributable, challenge-bound receipt.

Green CI is not a PJ002 PASS. A receipt is usable only after the PJ002 trust adapter verifies the GitHub artifact attestation and every frozen binding.

## Fail-closed rules

- No payload -> workflow fails.
- Subject/corpus/verifier hash mismatch -> workflow fails.
- Missing event, attempt, or challenge -> workflow fails.
- Test runner nonzero exit -> workflow records non-PASS and the job fails after preserving evidence.
- No attestation -> no VERIFIED_EXTERNAL claim.
- This repository never grants governance, admission, merge, release, deployment, staging, production, or protected-action authority.

## Expected frozen payload

Place these files under `payload/` in a separately reviewed initialization step:

- `subject.tar.gz`
- `corpus.tar.gz`
- `verifier.tar.gz`
- `run.sh`
- `freeze.json`

The workflow is intentionally unusable for a positive result until that exact payload is added and hash-bound.