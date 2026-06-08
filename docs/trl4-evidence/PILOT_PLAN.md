# Pilot Plan

**Product:** True Structure Assurance OS
**Date:** 2026-06-08

---

## Pilot 0: Internal Synthetic Validation (Complete)

**Status:** Complete at TRL 4

**Goal:** Prove the core workflow end-to-end with synthetic data.

**Dataset:** defense-autonomy sample (`samples/defense-autonomy/`)

**Validation:**
- Gap detection produces expected gaps ✅
- Readiness score in expected range (50–85) ✅
- Report generated with disclaimer ✅
- Automated test suite passes ✅

**Outcome:** TRL 4 demonstrated.

---

## Pilot 1: Friendly Engineering Partner

**Status:** Planned (TRL 5 target)

**Goal:** Validate the platform on anonymized real engineering artifacts.

**Target partners:**
- Dual-use startup with autonomous system under development
- Test automation team in a defense-adjacent company
- Robotics company preparing CE certification

**What they provide:**
- Anonymized requirements document (Word or PDF)
- Existing test case list (Excel or Jira export)
- Test execution results (CSV or JSON)
- Optional: existing manual traceability matrix

**What we measure:**
- AI extraction precision vs. partner's existing requirements list (target: >80%)
- AI trace suggestion accuracy vs. partner's existing traceability (target: >75%)
- Time to generate first readiness report (target: <2 hours from data upload)
- Partner rating of report usefulness (target: >3.5/5)
- Number of gaps found that partner was not previously aware of

**Duration:** 4–6 weeks per partner
**Target:** 2 partners completed within 4 months of TRL 4 validation

---

## Pilot 2: Dual-Use / Defense-Relevant Partner

**Status:** Planned (TRL 5/6 target)

**Goal:** Validate relevance for defense mission or certification readiness.

**Target partners:**
- Defense innovation unit (DIU) program
- Autonomous system developer with active mission validation effort
- Defense system integrator V&V team

**What we validate:**
- Platform fits into existing V&V workflow
- Readiness report is accepted as useful by program/mission lead
- Gap detection catches gaps that matter to the partner's mission/certification authority

**Duration:** 8–12 weeks
**Target:** 1 partner within 6 months of TRL 5 demonstration

---

## Pilot 3: Regulated Industry Partner

**Status:** Planned (TRL 6 target)

**Goal:** Prove dual-use expansion into civilian regulated industries.

**Target sectors:** Aerospace (DO-178C), medical device (IEC 62304), railway (EN 50128), industrial automation (IEC 61508)

**What we validate:**
- Platform handles sector-specific requirements and evidence formats
- Readiness report is useful for certification review preparation
- Gap detection identifies sector-relevant gaps (e.g., stale evidence thresholds apply correctly)

**Duration:** 8–12 weeks
**Target:** 1 partner within 9 months of TRL 5 demonstration

---

## Pilot Success Metrics

| Metric | Target |
|--------|--------|
| AI extraction precision | > 80% vs. human review |
| AI trace suggestion precision | > 75% vs. human review |
| Time to first readiness report | < 2 hours from data upload |
| Report usefulness rating | > 3.5 / 5 from engineering team |
| Gaps found that partner missed | ≥ 1 per pilot |
| Time saved vs. manual approach | > 30% reduction in evidence preparation |
| User acceptance | Engineer would use again: yes > 80% |
