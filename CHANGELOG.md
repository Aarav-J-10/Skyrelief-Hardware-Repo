# Change log
## 1.0.0 / 2026-10-21
- Applied the licensing scheme approved by both authors: CERN-OHL-W-2.0 (hardware design sources), MIT (software), CC-BY-4.0 (documentation, photographs, data). Canonical texts in `LICENSES/`; per-file assignment in `LICENSE_MATRIX.csv` and `REUSE.toml`; SPDX headers on all new code. Decision recorded in `AUTHOR_LICENSING_DECISIONS.md` (replaces `AUTHORS_LICENSING_APPROVAL_REQUIRED.md`).
- `release_gate.py` now verifies licence texts against canonical hashes, SPDX headers against the matrix, and REUSE metadata; D01–D05 and vendor artwork remain excluded and unlicensed.
- `check_release_lock.py`: GO now requires recovered historical sources or a recorded editorial ruling; new negative tests for licence substitution, licensing D01–D05 and a v1 tag without approval.
- Added a tag-triggered release workflow that builds the source archive and SHA-256 records.
- R01 geometry unchanged; regenerated and re-audited.

## 0.2.0-rc1 / 2026-10-20 (untagged release candidate)
- Restored `.gitignore` (listed in the 0.1.0 manifest but dropped by the GitHub web upload, which made the validator fail on the public tree) and added `.gitattributes` so released bytes are not rewritten.
- Added the shared `PUBLICATION_RELEASE_LOCK.json`, `PUBLICATION_GATE.md` and `AUTHORS_LICENSING_APPROVAL_REQUIRED.md`, identical in both repositories, plus `scripts/check_release_lock.py` (cross-repository comparison with seven negative tests).
- Added `scripts/release_gate.py`: screens the tree and every Git blob against withheld-CAD hashes and prohibited file types, and generates `LICENSE_MATRIX.csv` (all files `PUBLIC_LICENSE_APPROVAL_PENDING`).
- Added GitHub Actions CI and `scripts/write_file_manifest.py`; validators now skip `.git` and fail cleanly on missing files.
- Rewrote README around a five-minute reproduction path.
- Regenerated R01 exports (byte-identical apart from line endings) and added `scripts/independent_step_audit.py`: 26 checks from the STEP files alone, including a 0.25 mm interference sweep and a verified 16–20 mm release window.
- Added `scripts/render_two_state_figure.py` and `drawings/R01_two_state.{svg,pdf,png}`.
- New docs: R01 design definition, generator and parameters, design analysis, assembly instructions, build costs, system architecture, third-party components, rights disposition, verification report.

## 0.1.0-review / 2026-10-20
- Fresh immutable snapshot of all 49 upstream files with Git blob and SHA-256 verification.
- Evidence ledger, normalized parts/cost crosswalk, photo curation and rights exclusions.
- New independent editable engineering references separated from historical evidence.
- Actual native/digital checks and completed limitations matrix; no new physical tests.
