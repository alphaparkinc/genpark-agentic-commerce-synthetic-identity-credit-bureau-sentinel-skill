# Commerce Synthetic Identity Fraud & Tradeline Sentinel Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Synthetic identity theft (Frankenstein ID) detection, SSN issuance year vs. DOB mismatch scoring, piggybacking tradeline anomaly auditing, and BNPL credit application gatekeeper. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `screen_synthetic_identity_risk`: Analyze credit bureau applicant telemetry (SSN randomization timeline, authorized user tradeline count, velocity) to flag synthetic Frankenstein identities.
- `enforce_synthetic_id_countermeasure`: Enforce e-KYC step-up authentication (SSA-89 Social Security direct consent match, physical utility bill verification).

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_agentic_commerce_synthetic_identity_credit_bureau_sentinel_skill.server --test
```
