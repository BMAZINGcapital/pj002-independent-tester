import fs from 'node:fs';
import crypto from 'node:crypto';

const env = process.env;
const resultPath = 'out/test-result.json';
if (!fs.existsSync(resultPath)) throw new Error('Missing out/test-result.json');
const resultBytes = fs.readFileSync(resultPath);
const result = JSON.parse(resultBytes.toString('utf8'));
const allowed = new Set(['PASS','FAIL','BLOCKED','UNKNOWN']);
if (!allowed.has(result.decision)) throw new Error('Invalid decision');

function need(name) {
  const v = env[name];
  if (!v) throw new Error(`Missing ${name}`);
  return v;
}

const receipt = {
  schema_version: 'pj002-independent-receipt.v1',
  event_id: need('PJ002_EVENT_ID'),
  attempt_id: need('PJ002_ATTEMPT_ID'),
  challenge_nonce: need('PJ002_CHALLENGE_NONCE'),
  subject_sha256: need('PJ002_SUBJECT_SHA256'),
  corpus_sha256: need('PJ002_CORPUS_SHA256'),
  verifier_sha256: need('PJ002_VERIFIER_SHA256'),
  evidence_root: need('PJ002_EVIDENCE_ROOT'),
  result_sha256: crypto.createHash('sha256').update(resultBytes).digest('hex'),
  workflow_repository: need('GITHUB_REPOSITORY'),
  workflow_ref: need('GITHUB_WORKFLOW_REF'),
  workflow_sha: need('GITHUB_SHA'),
  workflow_run_id: need('GITHUB_RUN_ID'),
  workflow_run_attempt: need('GITHUB_RUN_ATTEMPT'),
  runner_environment: 'github-hosted',
  issued_at: new Date().toISOString(),
  decision: result.decision,
  test_result: result
};

fs.writeFileSync('out/receipt.json', JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify(receipt, null, 2));