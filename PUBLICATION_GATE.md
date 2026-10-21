# SkyRelief publication gate

Identical in both repositories. Re-assessed 2026-10-21 for release 1.0.0 against MDPI *Hardware* requirements as captured on 2026-10-20 (the official pages returned HTTP 403 to automated access; the authors should re-read the live wording before submission).

## Red lines (never relaxed)

1. No invented measurement, trial record, pin map, firmware setting, licence, approval, tag, DOI or push.
2. D01–D05 historical STEP files, their renders and any derivative geometry stay out of every public tree, release and supplement, and are not licensed, until the rights holder grants permission in writing.
3. R01 and the KiCad reference sheets are called new, unbuilt references wherever they appear.
4. 19/20 is a retrospective composite count only. No separate release, detection or avoidance rate. The unsupported 97% release figure is not used.
5. The nine scout ERC errors stay visible. No `no_connect` flag or guessed net silences them.
6. Numerical scenarios are never presented as aircraft measurements.
7. Author licensing approval is not approval of manuscript text, and is not evidence that construction or operating sources exist.

## Hard gates

| Gate | Requirement | Status | Evidence / blocker |
|---|---|---|---|
| G01 | Scope fits *Hardware* | **AT RISK** | Retrospective UAV integration plus decision model; needs the editor's view |
| G02 | Editable original construction sources for the device claimed built, under an open licence | **FAIL** | Licensing is now done for everything the authors own, but the historical frame CAD is third-party and withheld, and the latch and harness were never drawn. R01/KiCad are licensed new references, not the built device. |
| G03 | Software needed to operate the device | **FAIL** | No ArduPilot parameters, Betaflight dump, mission file, release trigger or perception code was recovered |
| G04 | Demonstration of fitness for purpose at the level claimed | **CONDITIONAL** | Photographs establish two built aircraft and a latch; 19/20 is unregistered. Holds only at "constructed prototype" claim level |
| G05 | Supplements attached, licensed, version-locked, usable | **PASS for S1/S2; S3 unverified** | Licensed v1.0.0 releases; S3 not supplied to the release audit |
| G06 | Both authors approve the final manuscript; exclusivity and prior-submission statements | **PENDING** | Licensing approval does not cover the revised manuscript |
| G07 | Manuscript and supplements pass citation, equation, figure and sync audits | **PASS (candidate)** | See compliance report |
| G08 | No unapproved redistribution, fake claim or invented licence | **PASS** | `release_gate.py` over tree and Git history; licences match the recorded decision |

## Verdict

**Formal submission: NO-GO.** **Pre-submission eligibility inquiry: CONDITIONAL GO.** Licensing readiness is resolved; hardware reproducibility of the historical aircraft is not. G02 and G03 require recovered historical sources or a written editorial ruling on a narrowed claim set.
