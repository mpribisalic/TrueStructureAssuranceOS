# Risk Register

**Product:** True Structure Assurance OS TRL 4 Prototype
**Date:** 2026-06-08

---

## Project Risks

| ID | Risk | Severity | Likelihood | Level | Mitigation | Status |
|----|------|----------|-----------|-------|-----------|--------|
| R-001 | Mock AI gives false confidence — evaluators may assume real AI accuracy | medium | possible | medium | Clearly label mock AI in UI and reports; document limitation in TRL4_READINESS_ASSESSMENT | mitigated |
| R-002 | OpenAI API costs become prohibitive at scale | medium | possible | medium | Mock provider as default; OpenAI optional; future local LLM interface prepared | mitigated |
| R-003 | AI prompt injection via uploaded documents | high | unlikely | medium | System prompt includes untrusted-input instruction; output validated against schema; human review required | mitigated |
| R-004 | Scoring formula is gamed or misunderstood | medium | unlikely | low | Formula fully documented; deterministic; explanation generated with every score | mitigated |
| R-005 | Demo environment fails during DIANA presentation | high | unlikely | medium | Demo script uses seeded deterministic data; mock AI; no internet needed | mitigated |
| R-006 | Data privacy concern with real engineering artifacts | high | possible | high | TRL 4 uses synthetic data only; pilot stage uses anonymized data; no real classified data at any TRL | open |
| R-007 | Stack dependency vulnerabilities | medium | possible | medium | Automated dependency updates (Dependabot); regular security scan before pilot | open |
| R-008 | Performance degradation with large projects (>100 requirements) | medium | possible | medium | Not tested at TRL 4; flagged as known limitation; performance testing planned for TRL 5 | open |

---

## Risk Level Matrix

```
Likelihood →    Rare    Unlikely  Possible  Likely  Almost certain
Severity ↓
Catastrophic    Med     High      Critical  Crit    Critical
Critical        Low     Med       High      Crit    Critical
High            Low     Med       High      High    Critical
Medium          Low     Low       Med       High    High
Low             Low     Low       Low       Med     Med
```

---

## Open Risks

R-006, R-007, R-008 remain open. They are acceptable for TRL 4 (lab prototype with synthetic data). They must be addressed before TRL 5 pilot with real engineering partners.
