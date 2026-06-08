# Dual-Use Technology Positioning — True Structure Mission Assurance Platform

**Version:** 1.0  
**Date:** 2026-06-08  
**Classification:** Unclassified / Public  

---

## 1. Technology Summary

The True Structure Mission Assurance Platform is a mission assurance and readiness intelligence platform that transforms unstructured engineering artifacts into traceable, explainable certification evidence chains. The platform automates the collection, linkage, and gap analysis of requirements, test cases, and evidence records, producing deterministic readiness scores and structured reports for use by evaluators, auditors, and program offices.

The core technology is domain-agnostic: any engineering program that must demonstrate that requirements are tested, evidence exists, and gaps are tracked can benefit from the platform. This positions the technology as inherently dual-use — immediately applicable to defense autonomous systems certification and equally applicable to regulated civil industries operating under safety-critical standards.

---

## 2. Defense Applications

### Autonomous Unmanned Systems Validation

Unmanned aerial vehicles (UAS), unmanned ground vehicles (UGV), and unmanned surface vessels (USV) require systematic validation of autonomous behaviours before operational deployment. True Structure provides:

- Structured requirement capture for autonomy-specific behaviours (GPS-denied navigation, sensor disagreement handling, fail-safe return)
- Integration with simulation-based test environments (ArduPilot SITL and equivalent)
- Gap detection tuned to defense autonomy standards: missing safety tests, missing security tests, failed simulation runs
- Mission impact analysis translating engineering gaps into operational risk language

### NATO Certification Readiness

Defense programs seeking NATO certification or acceptance face rigorous documentation requirements. True Structure addresses:

- STANAG compliance tracking (requirements tagged to applicable standards)
- Traceable evidence chains for auditor review
- Explainable readiness scores with full audit trail
- Report generation formatted for program office submission

### Safety-Critical Defense Software

Avionics, weapons system software, and command and control systems governed by DO-178C (airborne software), MIL-STD-882 (system safety), and related standards require structured evidence of test coverage. True Structure provides:

- Criticality-aware gap detection (catastrophic and critical requirements receive stricter caps)
- Stale evidence detection calibrated to criticality level (critical requirements: 30-day threshold)
- Human-in-the-loop review gates ensuring AI suggestions are validated before affecting scores

### Trusted Autonomy and AI Assurance

As defense programs incorporate AI decision-making into autonomous systems, new assurance challenges arise. True Structure provides a framework for:

- Capturing AI behaviour requirements and linking them to test cases
- Importing evidence from AI-in-the-loop simulation runs
- Detecting gaps in AI system test coverage using the same deterministic rules as conventional software

---

## 3. Civil Applications

The same evidence chain management and readiness intelligence capabilities that serve defense programs are directly applicable to civil regulated industries:

### Aerospace Software Certification (DO-178C / DO-254)

- Requirements-to-test traceability with human review gates
- Evidence management for software test records
- Coverage analysis and gap detection aligned to DO-178C objectives

### Automotive Functional Safety (ISO 26262)

- Safety requirement management with ASIL (Automotive Safety Integrity Level) criticality mapping
- Hardware and software test evidence import and linkage
- Gap detection for missing safety analysis artifacts

### Medical Device Software (IEC 62304)

- Software lifecycle process evidence capture
- Risk-based gap detection (Class A / B / C severity mapping)
- Audit-ready report generation for regulatory submissions

### Railway Systems (EN 50128)

- Software safety integrity level (SIL) aware requirements management
- Test evidence linkage and gap detection for V-model artefacts
- Readiness scoring against certification milestones

### Industrial Safety Systems (IEC 61508)

- Functional safety requirement management across hardware and software
- Evidence chain management for safety lifecycle documentation
- Gap detection for missing verification and validation records

---

## 4. Market Analysis

### Defense V&V Market

The defense verification and validation (V&V) software market is growing due to the rapid proliferation of autonomous systems across all domains. Key drivers include:

- Increasing adoption of UAS, UGV, and USV platforms in NATO member forces
- Regulatory pressure for documented autonomy assurance (NATO STANAG, US DoD AI Ethics principles)
- Growing complexity of autonomous system certification — traditional tools are not designed for the evidence chain requirements of autonomous behaviour validation

### Civil Certification Market

Regulatory pressure is increasing across all safety-critical civil sectors simultaneously:

- DO-178C and DO-254 certification cycles typically consume 40–60% of avionics program budgets in documentation and evidence management
- ISO 26262 adoption is accelerating beyond automotive OEMs into Tier 1 and Tier 2 suppliers
- IEC 62304 enforcement is tightening as medical AI software comes under scrutiny from FDA and European regulators

### Core Pain Point

Manual evidence collection, traceability management, and gap analysis in certification programs typically costs months of senior engineering time per certification cycle. The gap between the first test execution and the final certification submission is filled with manual spreadsheets, email trails, and document hunting — activities that True Structure automates and makes auditable.

---

## 5. Competitive Differentiation

### Existing Tooling

| Tool | Category | Gap |
|------|----------|-----|
| IBM DOORS / DOORS Next | Requirements management | No readiness intelligence, no gap detection, no evidence chain |
| Jira | Issue tracking | No certification context, no traceability semantics |
| Confluence | Documentation | No structured evidence management, no scoring |
| TestRail / Zephyr | Test management | No requirements-to-evidence chain, no readiness scoring |
| Microsoft Excel | Manual tracking | Not auditable, not scalable, no AI assistance |

None of the existing tools are purpose-built for the complete requirements → test → evidence → gap → readiness → report chain that certification and mission assurance programs require.

### True Structure Differentiation

- **Purpose-built for certification evidence chains** — not a generic project management tool adapted for compliance
- **Deterministic gap detection** — 7 rules produce reproducible, auditable results; no black-box scoring
- **AI-assisted with human-in-the-loop gates** — AI suggestions for requirement extraction and traceability accelerate engineering work without removing human accountability
- **Mission impact analysis** — engineering gaps are translated into operational consequence language, enabling program managers to prioritise remediation by mission risk rather than engineering metrics
- **Explainable readiness scores** — every score includes the exact caps applied, component scores, and recommended actions; no opaque scoring
- **Simulation test integration** — ATVP connector closes the loop between physical/simulation test execution and certification documentation

---

## 6. NATO DIANA Alignment

### Trusted Autonomy Priority

NATO has identified trusted autonomy as a priority technology area. The core challenge is demonstrating that autonomous systems will behave as intended in adversarial environments. True Structure directly addresses this challenge by providing a platform for capturing, validating, and reporting on the evidence that autonomous system behaviours have been tested and any gaps have been identified.

### Dual-Use Value Proposition

- **Immediate defense value:** Autonomous UAS/UGV/USV programs can use the platform today to manage STANAG and DO-178C certification evidence
- **Large civil market:** The same platform applies to aerospace, automotive, medical device, and railway certification without modification — addressable civil market is orders of magnitude larger than the defense segment alone
- **Network effects:** Civil pilot customers generate domain-specific gap detection rules and report templates that improve the platform for all users, including defense programs

### TRL Path

| Phase | TRL | Milestone |
|-------|-----|-----------|
| Current (Phase 20) | 4 | Reproducible lab demonstration with ARSP dataset, 97/97 tests passing |
| Phase 21–22 | 5 | Pilot deployment with defense contractor, real program data, OpenAI provider enabled |
| Phase 23–25 | 6 | Two pilot customers (defense + civil), production deployment, multi-tenant isolation |
| Phase 26+ | 7–8 | Program office adoption, integration with government data systems |

---

## 7. Pilot Strategy

### Phase 1: Defense Contractor Pilot

**Target:** Autonomous UAS program at a NATO-member defense contractor  
**Objective:** Validate the platform against real program data under NDA; demonstrate readiness score accuracy against expert assessor judgement  
**Success criteria:** Program team adopts the platform for one certification milestone; at least one gap is identified before it would have been found by manual review  

### Phase 2: Civil Aerospace Pilot

**Target:** DO-178C certification project at a civil avionics supplier  
**Objective:** Validate the platform's gap detection and readiness scoring for DO-178C DAL A/B software  
**Success criteria:** Evidence import from existing test management tool; readiness score aligned with independent DER (Designated Engineering Representative) assessment  

### Phase 3: NATO Program Office Pilot

**Target:** NATO agency or national program office managing an autonomous systems acquisition  
**Objective:** Validate report format and evidence chain structure against program office acceptance criteria  
**Success criteria:** Program office accepts platform-generated certification readiness report as sufficient for TRL gate review  
