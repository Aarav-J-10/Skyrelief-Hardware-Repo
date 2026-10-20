# Licensing decisions required from both authors

Nothing in either repository is licensed for reuse until **both** Aarav Jalan and Abhinav Patro sign off below. Publication consent for your own material (already given) is not a licence. Tick one option per row, or write your own.

| # | Material | Files | Options | Notes |
|---|---|---|---|---|
| 1 | New hardware design source (R01 CAD, KiCad projects, drawings) | `cad/independently_authored/*`, `drawings/R01_*`, `kicad/*` | ☐ CERN-OHL-W-2.0 ☐ CERN-OHL-S-2.0 ☐ CERN-OHL-P-2.0 | -S requires modified hardware to stay open (strongly reciprocal); -W is reciprocal only for the design itself; -P is permissive. These were generated with AI assistance under your direction: confirm you accept authorship. |
| 2 | Scripts (generator, validators, release tools, historical estimate script) | `scripts/*.py`, `evidence/original/*.py` | ☐ MIT ☐ Apache-2.0 | The historical script is credited to A. Patro: his decision governs it. |
| 3 | Documentation, tables, diagrams | `docs/*`, `bom/*`, `data/*`, `verification/*`, `diagrams/*` | ☐ CC BY 4.0 ☐ CC BY-SA 4.0 | |
| 4 | Project photographs and component-list PDFs | `images/*`, `evidence/original/*.pdf`, `assets/*` | ☐ CC BY 4.0 ☐ publish-only (all rights reserved) | Confirm no identifiable person appears without consent. |
| 5 | Archived thrust data | `evidence/original/Thrust_Test_1.ods`, `data/archived_thrust_sheet_transcription.csv` | ☐ CC0 1.0 ☐ CC BY 4.0 | |
| 6 | D01–D05 historical STEP | not in repository | Not yours to license unless you are the creator | Ask the creator named in the metadata ("Brayo") or the source you downloaded them from. |

After signing, record the choice in `LICENSES.md`, add SPDX headers, set `rights_status.overall` to `APPROVED` in `PUBLICATION_RELEASE_LOCK.json` in both repositories, regenerate `LICENSE_MATRIX.csv`, and only then tag a release.

| Author | Decision recorded | Date |
|---|---|---|
| Aarav Jalan | | |
| Abhinav Patro | | |
