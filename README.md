# PJ002 Independent Tester

External evidence and independent-runner surface for PRIMAL JUNGLE 002.

## Frozen source

This tester is bound to the exact PJ002-E006 frozen source lineage:

`44143d61b632c0d3810d44a40c78f5911b1a8921`

Frozen payload:

- `payload/subject.zip`
- `payload/corpus.zip`
- `payload/verifier.zip`
- `payload/freeze.json`
- `payload/bindings.json`

## Two-phase trust path

1. A GitHub-hosted runner verifies the exact frozen payload.
2. It creates an external decision bound to a fresh proof, attempt, challenge and evidence root.
3. GitHub/Sigstore attests that decision.
4. A second job verifies the attestation against this exact repository/workflow.
5. Only after successful attestation verification is `decision_receipt_authenticated=true` created.
6. The exact frozen E006 verifier/corpus is replayed.
7. The final result is separately attested.

A green GitHub workflow does not grant governance, admission, merge, release, deployment, staging or production authority.

Historical PJ002 E001-E006 evidence remains immutable.