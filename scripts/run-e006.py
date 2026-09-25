import copy
import hashlib
import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

with open(OUT / "verified-trust.json", "r", encoding="utf-8") as f:
    verified_trust = json.load(f)

with zipfile.ZipFile(ROOT / "payload" / "corpus.zip") as z:
    with tempfile.TemporaryDirectory() as td:
        z.extractall(td)
        corpus = json.load(open(pathlib.Path(td) / "corpus.json", encoding="utf-8"))
        oracle = json.load(open(pathlib.Path(td) / "oracle.json", encoding="utf-8"))

with zipfile.ZipFile(ROOT / "payload" / "verifier.zip") as z:
    with tempfile.TemporaryDirectory() as td:
        z.extractall(td)
        verifier_path = pathlib.Path(td) / "verifier.py"

        spec = importlib.util.spec_from_file_location("pj002_e006_verifier", verifier_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        expected = {
            x["case_id"]: x["expected"]
            for x in oracle["expected_results"]
        }

        base_trust = verified_trust["trust_result"]

        anchor = {
            "event_id": "PJ002-E006",
            "authorized_attempt_id": base_trust["attempt_id"],
            "authorized_challenge_nonce": base_trust["challenge_nonce"],
            "clock_domain_identity": base_trust["clock_domain_identity"],
            "evidence_root_identity": base_trust["evidence_root_identity"]
        }

        results = []

        for case in corpus["cases"]:
            cid = case["id"]
            trust = copy.deepcopy(base_trust)
            local_anchor = copy.deepcopy(anchor)

            if cid == "PJ002-T001":
                trust = {}

            elif cid == "PJ002-T002":
                trust["adapter_source"] = "SUBJECT_GENERATED"

            elif cid == "PJ002-T003":
                trust["adapter_source"] = "REPO_LOCAL_ONLY"

            elif cid == "PJ002-T004":
                trust["event_id"] = "WRONG-EVENT"

            elif cid == "PJ002-T005":
                trust["attempt_id"] = "WRONG-ATTEMPT"

            elif cid == "PJ002-T006":
                trust["challenge_nonce"] = "WRONG-CHALLENGE"

            elif cid == "PJ002-T007":
                trust["clock_domain_identity"] = "WRONG-CLOCK-DOMAIN"

            elif cid == "PJ002-T008":
                trust["evidence_root_identity"] = "WRONG-EVIDENCE-ROOT"

            elif cid == "PJ002-T009":
                trust["decision_receipt_authenticated"] = False
                trust["decision_authentication_reference"] = ""

            elif cid == "PJ002-T010":
                trust["trust_decision"] = "INVALID_EXTERNAL"

            elif cid == "PJ002-T011":
                trust["trust_decision"] = "UNKNOWN"

            elif cid == "PJ002-T012":
                trust["trust_decision"] = "BLOCKED"

            elif cid == "PJ002-T013":
                pass

            observed = module.verify(case, trust, local_anchor)
            exp = expected[cid]

            results.append({
                "case_id": cid,
                "expected": exp,
                "observed": observed["result"],
                "matched": observed["result"] == exp,
                "reason": observed["reason"]
            })

        matched = sum(1 for r in results if r["matched"])

        result = {
            "schema_version": "pj002-e006-external-replay.v1",
            "source_event": "PJ002-E006",
            "external_proof_id": os.environ["PJ002_PROOF_ID"],
            "attempt_id": base_trust["attempt_id"],
            "challenge_nonce": base_trust["challenge_nonce"],
            "evidence_root_identity": base_trust["evidence_root_identity"],
            "cases_total": len(results),
            "cases_matched": matched,
            "decision": "PASS" if matched == len(results) else "FAIL",
            "results": results,
            "limitations": [
                "TRUST_ADAPTER_GATE_ONLY",
                "NATIVE_BEHAVIOR_NOT_PROVEN",
                "NO_GOVERNANCE_AUTHORITY",
                "NO_ADMISSION_AUTHORITY",
                "NO_DEPLOYMENT_AUTHORITY"
            ]
        }

        with open(OUT / "test-result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, sort_keys=True)
            f.write("\n")

        print(json.dumps(result, indent=2))