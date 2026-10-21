# Licences

Release 1.0.0 is open-licensed. Both authors, Aarav Jalan and Abhinav Patro, approved the scheme on 21 October 2026 ([decision record](AUTHOR_LICENSING_DECISIONS.md)). Every file's licence and copyright holder is listed in [`LICENSE_MATRIX.csv`](LICENSE_MATRIX.csv) and, machine-readably, in [`REUSE.toml`](REUSE.toml) ([REUSE](https://reuse.software/) 3.x format).

| Material | Licence | Text |
|---|---|---|
| Hardware design sources: R01 CAD (parameters, STEP exports), R01 drawings and R01 documentation | CERN Open Hardware Licence v2 – Weakly Reciprocal (`CERN-OHL-W-2.0`) | [LICENSES/CERN-OHL-W-2.0.txt](LICENSES/CERN-OHL-W-2.0.txt) |
| Software: CAD generator, validators, release tools, CI configuration, and the historical endurance-estimate script | MIT (`MIT`) | [LICENSES/MIT.txt](LICENSES/MIT.txt) |
| Documentation, tables, diagrams, illustrations, project photographs, component lists and archived data | Creative Commons Attribution 4.0 International (`CC-BY-4.0`) | [LICENSES/CC-BY-4.0.txt](LICENSES/CC-BY-4.0.txt) |

Copyright: new files © 2026 Aarav Jalan and Abhinav Patro; historical project files © 2024–2025 Aarav Jalan and Abhinav Patro; the historical estimate script © 2024–2025 Abhinav Patro. Attribute as "SkyRelief, Aarav Jalan and Abhinav Patro" with a link to this repository and release.

## Not licensed by this repository

| Material | Status |
|---|---|
| D01–D05 historical STEP files (four with "Brayo" / Inventor 2022 metadata, one with blank author) and any render, mesh or traced geometry | **Withheld**; not present; the authors cannot license them. See [exclusions](docs/EXCLUDED_THIRD_PARTY_CAD.md). |
| Vendor/tutorial artwork (JHEMCU illustration, HAWK'S WORK motor graphic, catalogue images) | **Excluded**; cited by name only |
| KiCad, Open CASCADE, ArduPilot, Betaflight and other upstream tools | Not redistributed; their own licences apply |
| Trademarks (Pixhawk, DJI, FlySky, RadioMaster, TowerPro, etc.) | Identify equipment only; no endorsement |

`scripts/release_gate.py` regenerates the matrix and `REUSE.toml`, checks the licence texts against the canonical SPDX texts, and screens the tree and Git history for withheld files. A licence on these files says nothing about whether the historical aircraft can be reproduced; see [the publication gate](PUBLICATION_GATE.md).
