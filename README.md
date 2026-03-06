# QA Test Infrastructure — Senior Full Stack QA Portfolio

> A production-grade test infrastructure demonstrating senior-level QA architecture 
> across Backend, Data, Frontend, and AI/ML layers.

## Why This Architecture?

| Tool | Alternative | Reason Chosen |
|---|---|---|
| **Playwright** | Selenium | Native async, built-in trace viewer, no WebDriver dependency |
| **httpx + pytest-asyncio** | requests | FastAPI is async-first; blocking requests miss race conditions |
| **SQLAlchemy 2.0 async** | Raw SQL | Type-safe, testable via dependency injection overrides |
| **Evidently/Streamlit** | Manual logs | Statistical drift detection; binary pass/fail is insufficient for ML |

## Repo Structure
- `phase1_backend/` — FastAPI async test suite with 90%+ coverage gate
- `phase2_data/` — ACID compliance, migration validation, NoSQL consistency tests
- `phase3_frontend/` — Playwright POM with auth state caching
- `phase4_ai_ml/` — Streamlit model monitoring dashboard with drift detection
- `phase5_integration/` — CI/CD pipeline + quality risk report template

## CI/CD Pipeline
Linter (Ruff/Black) → Unit Tests (90% cov gate) → Integration Tests → Security Scan (Bandit)

## Quality Risk Assessment (Sample)
- ✅ Backend API: 94% coverage, all ACID rollbacks verified
- ✅ Frontend: POM-based, auth state cached, network-intercepted
- ⚠️ AI Model: F1=0.82 (above 0.80 threshold), monitor drift weekly
- 🚨 DB Migration: `down_revision` rollback path not yet tested in staging

## Setup
```bash
git clone https://github.com/pranavyk10/qa-test-infrastructure
cd qa-test-infrastructure
pip install -r requirements.txt
playwright install chromium
