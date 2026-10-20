# -*- coding: utf-8 -*-
"""MCP Server for Commerce Synthetic Identity Fraud & Tradeline Sentinel Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import SyntheticIdentityCreditBureauSentinel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "screen_synthetic_identity_risk",
        "description": "Analyze credit bureau applicant telemetry (SSN randomization timeline, authorized user tradeline count, velocity) to flag synthetic Frankenstein identities.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "applicant_id": {
                    "type": "string"
                },
                "applicant_dob_year": {
                    "type": "integer"
                },
                "ssn_estimated_issuance_year": {
                    "type": "integer"
                },
                "authorized_user_tradelines_count": {
                    "type": "integer",
                    "description": "Piggybacking tradelines count"
                },
                "primary_tradelines_count": {
                    "type": "integer"
                },
                "credit_file_depth_months": {
                    "type": "integer"
                }
            },
            "required": [
                "applicant_id",
                "applicant_dob_year",
                "ssn_estimated_issuance_year",
                "authorized_user_tradelines_count",
                "primary_tradelines_count"
            ]
        }
    },
    {
        "name": "enforce_synthetic_id_countermeasure",
        "description": "Enforce e-KYC step-up authentication (SSA-89 Social Security direct consent match, physical utility bill verification).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "applicant_id": {
                    "type": "string"
                },
                "synthetic_risk_score": {
                    "type": "number"
                },
                "flagged_anomalies": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": [
                "applicant_id",
                "synthetic_risk_score",
                "flagged_anomalies"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-synthetic-identity-credit-bureau-sentinel-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(SyntheticIdentityCreditBureauSentinel, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-agentic-commerce-synthetic-identity-credit-bureau-sentinel-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-synthetic-identity-credit-bureau-sentinel-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
