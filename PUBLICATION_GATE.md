# SkyRelief publication gate

Identical in both repositories. Assessed 2026-10-20 against MDPI *Hardware* requirements as captured that day (the official pages returned HTTP 403 to automated access; wording was taken from publisher-indexed text and must be re-read by the authors before submission).

## Red lines (never relaxed)

1. No invented measurement, trial record, pin map, firmware setting, licence, approval, tag, DOI or push.
2. D01–D05 historical STEP files, their renders and any derivative geometry stay out of every public tree and supplement until the rights holder grants permission in writing.
3. R01 and the KiCad reference sheets are called new, unbuilt references wherever they appear.
4. 19/20 is a retrospective composite count only. No separate release, detection or avoidance rate. The unsupported 97% release figure is not used.
5. The nine scout ERC errors stay visible. No `no_connect` flag or guessed net silences them.
6. Numerical scenarios are never presented as aircraft measurements.

## Hard gates

| Gate | Requirement | Status | Evidence / blocker |
|---|---|---|---|
| G01 | Scope fits *Hardware* (open-source scientific/laboratory hardware, novel device) | **AT RISK** | Retrospective UAV integration plus decision model; journal emphasis since 17 Sep 2026 is duplicable open designs. Needs editor's view. |
| G02 | Editable original construction sources for the device claimed built, under an open licence | **FAIL** | Historical frame CAD withheld (rights); latch never drawn; no licence elected for anything. R01/KiCad are new references, not the built device. |
| G03 | Software needed to operate the device | **FAIL** | No ArduPilot parameter file, Betaflight dump, mission file, release trigger or perception code recovered. |
| G04 | Demonstration of fitness for purpose at the level claimed | **CONDITIONAL** | Photographs establish two built aircraft and a latch; 19/20 is unregistered. Acceptable only if claims stay at "constructed prototype" level. |
| G05 | Supplements attached, licensed, version-locked, usable | **FAIL (licence) / PASS (content)** | S1/S2 build and verify from these trees; S3 not supplied to this session; no licence. |
| G06 | Both authors approve the final manuscript; exclusivity and prior-submission statements | **PENDING** | Earlier approvals do not cover this revision. |
| G07 | Manuscript and supplements pass citation, equation, figure and sync audits | **PASS (candidate)** | See compliance report: editable DOCX with native equations, PDF from the same DOCX, cross-repo lock check. |
| G08 | No unapproved redistribution, fake claim or invented licence | **PASS** | `scripts/release_gate.py` screens tree and Git history; no licence file asserts approval. |

## Secondary gates

| Gate | Status |
|---|---|
| S01 Costed BOM, qualified | PASS — partial baskets INR 18,428 / INR 5,920 / USD 115.95, no total |
| S02 ERC states documented | PASS — 0 / 0 / 9 (KiCad 9.0.9 re-run) |
| S03 R01 recomputed | PASS — byte-identical regeneration; 26-check independent audit |
| S04 Computational archive executed | **NOT VERIFIED** — archive not supplied; manuscript arithmetic independently recomputed (45/45) |
| S05 DOI / release citations real | PASS — none cited; none minted |
| S06 AI assistance and rights statements | PASS (pending author confirmation of wording) |
| S07 Figures, captions, equations, metadata | PASS (candidate) |
| S08 No numerical contradictions | PASS — sync matrix checked |

## Verdict

**CONDITIONAL GO for a pre-submission eligibility inquiry to the Editorial Office. NO-GO for a formal compliant submission today.** G02 and G03 cannot pass from surviving evidence; they need either an editorial ruling on a narrowed claim set or recovered sources, plus a licence election by both authors.

### Path to GO
1. Both authors elect licences (see `AUTHORS_LICENSING_APPROVAL_REQUIRED.md`).
2. The Editorial Office states in writing whether a retrospective integration article with new reference designs is eligible, and under which article type.
3. Both authors approve the final manuscript and confirm exclusivity.
4. Attach and verify S3; tag both repositories at the same release label.
