# SkyRelief / Mechanical hardware

**Historical SkyRelief hardware dossier with modern engineering reconstruction.** Source-supported components and connectivity are distinguished from new reference implementations. Unrecovered pin assignments, firmware parameters and code must not be treated as as-built records or electrically validated flight instructions.

Version **0.1.0-review**, created 20 October 2026. Historical source: [project archive](https://github.com/Shadowfax0707/project-ap-DDPDS_2024_1729-0707), main at **42f9a44600351ec6d0a57fb20756c547acf38cad**. All 49 source files freshly fetched and Git-blob verified; **12 author-attributed originals included here**. See [source manifest](data/source_manifest.csv).

**Review package: specific public reuse licences pending.** Five historical STEP models and external artwork are excluded. Read [licences](LICENSES.md), [known limitations](Known_Limitations.md), [exclusions](docs/EXCLUDED_THIRD_PARTY_CAD.md) and [issue matrix](data/issue_matrix.csv).

## Quick start
1. Read the [overview](docs/01_System_Overview.md), [source register](docs/Source_Document_Register.md), [photo map](docs/Photo_Map.md) and [BOM interpretation](bom/README.md).
2. Read [assembly guide](docs/04_Assembly_Guide.md) and [CAD instructions](cad/README.md). Install cadquery-ocp==8.0.1.1.0, then run: python cad/independently_authored/build_reference.py. Open the new STEP exports in a STEP-capable CAD editor.
3. Run **python scripts/validate_repository.py** from the repository root (Python 3.11+; standard library). Review [file results](verification/repository_checks.json).
4. Read [verification details](docs/08_Verification_Results.md) before using any result.

## Evidence and design scope
- Historical evidence: component lists, original photographs, entered ODS and illustrative estimate. They do not establish installed settings.
- Source-derived: functional diagrams, BOM/connection crosswalks and numerical audit facts.
- New reference: independent R01 bench gate, Python/JSON, three parts and two assembly states.
- Missing: actual CAD permissions, complete latch/harness, firmware/parameters, logs and deployed perception source. No fully reproducible autonomous replica is supplied.

## Documents
- [System overview](docs/01_System_Overview.md)
- [Mechanical architecture](docs/02_Mechanical_Architecture.md)
- [Payload retention and release](docs/03_Payload_Retention_and_Release.md)
- [Assembly and inspection guide](docs/04_Assembly_Guide.md)
- [Manufacturing and safety](docs/05_Manufacturing_and_Safety.md)
- [Assumptions and unknowns](docs/06_Design_Assumptions_and_Unknowns.md)
- [Provenance and rights](docs/07_Source_Provenance_and_Rights.md)
- [Verification results](docs/08_Verification_Results.md)
- [Manuscript artifact map](docs/09_Manuscript_Figure_and_Table_Map.md)

## Authors and citation
[CITATION.cff](CITATION.cff) identifies Aarav Jalan (Adani International School, Ahmedabad) and Abhinav Patro (SSRVM, Ahmedabad). This engineering reconstruction is for their review, not an already published release or DOI. See [contribution rules](CONTRIBUTING.md).

No new physical experiments, flight qualification, certification or journal submission-readiness determination is claimed.
