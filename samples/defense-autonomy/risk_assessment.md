# Risk Assessment — Autonomous Reconnaissance Sensor Platform

## RISK-001: Positioning Signal Loss
- **Severity:** High
- **Likelihood:** Medium
- **Risk Level:** High
- **Mitigation:** REQ-001 mandates 30-second safe operation window; verified by T-002.

## RISK-002: Communication Blackout
- **Severity:** High
- **Likelihood:** Medium
- **Risk Level:** High
- **Mitigation:** REQ-002 mandates 5-second detection and degraded mode entry; verified by T-003.

## RISK-003: Sensor Data Spoofing or Disagreement
- **Severity:** Critical
- **Likelihood:** Low
- **Risk Level:** High
- **Mitigation:** REQ-003 mandates safe mode on sensor disagreement; T-004 currently failing — remediation required.

## RISK-004: Unauthorized Command Injection
- **Severity:** Critical
- **Likelihood:** Low
- **Risk Level:** High
- **Mitigation:** REQ-005 mandates command rejection; no security test linked — gap identified.

## RISK-005: Missing Validation Audit Trail
- **Severity:** Medium
- **Likelihood:** Medium
- **Risk Level:** Medium
- **Mitigation:** REQ-008 mandates validation log after each run; partially covered.
