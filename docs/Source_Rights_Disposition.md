# Source rights disposition

Every file in the release is classified in [`LICENSE_MATRIX.csv`](../LICENSE_MATRIX.csv). This page summarises the classes. Both authors licensed their own material on 21 October 2026. Third-party material is excluded and unlicensed.

| Class | Files | Publication | Reuse licence | Who decides |
|---|---|---|---|---|
| Author-owned historical originals | `evidence/original/*`, `images/payload/*`, `images/scout/*` | Published | **CC-BY-4.0** | Approved by both authors |
| Author-owned historical script and data | `evidence/original/*.py`, `*.ods` | Published | **MIT** (script), **CC-BY-4.0** (data) | Approved by both authors |
| New R01 design source and exports | `cad/independently_authored/*`, `drawings/R01_*` | Published | **CERN-OHL-W-2.0** (generator code MIT) | Approved by both authors |
| New scripts | `scripts/*.py` | Published | **MIT** | Approved by both authors |
| New documentation and data tables | `docs/*`, `bom/*`, `data/*`, `verification/*` | Published | **CC-BY-4.0** | Approved by both authors |
| Historical STEP D01–D05 | not in repository | **Withheld** | Not ours to grant | Original creator(s); D01–D04 metadata names "Brayo" |
| Vendor/tutorial artwork | not in repository | **Excluded** | Not ours to grant | Respective owners |
| ArduPilot, Betaflight, KiCad, Open CASCADE | not redistributed | n/a | Upstream licences apply | Upstream projects |
| MDPI Word template / formatted manuscript | not in repository | Not posted | MDPI terms | MDPI |

## Lineage check for R01

`build_reference.py` imports only Open CASCADE primitive constructors (boxes, cylinders, Boolean operations, translations) and reads only `parameters.json`. It opens no STEP, mesh or image file. R01's topology (sliding gate in rails, keyhole aperture) differs from the D05 bracket's (base plate with two uprights and coaxial bores, as recorded in the private audit). This is evidence of independent geometry; it is not a legal opinion.

## Git history exposure

The withheld STEP binaries' SHA-256 values are listed in `data/withheld_asset_manifest.csv`. `scripts/release_gate.py` checks every file in the working tree **and every blob in Git history** against those hashes and against forbidden file types. As of this revision no withheld binary is present in either.
