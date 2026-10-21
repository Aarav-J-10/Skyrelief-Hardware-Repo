# Release notes — v1.0.0

**Mechanical hardware sources for SkyRelief, Supplement S1** of the manuscript *SkyRelief: A Human-Supervised Dual-UAV Delivery Prototype with Mission-Architecture Analysis* (A. Jalan, A. Patro; candidate for MDPI *Hardware*, not yet submitted). Paired with the same tag in [SkyRelief-Electronics-Integration-Repository](https://github.com/Aarav-J-10/SkyRelief-Electronics-Integration-Repository); both carry an identical `PUBLICATION_RELEASE_LOCK.json`.

## Licences
CERN-OHL-W-2.0 for hardware design sources, MIT for software, CC-BY-4.0 for documentation, photographs and data, approved by both authors on 21 October 2026. See `LICENSES.md` and `LICENSE_MATRIX.csv`.

## What you can reproduce
- **R01**, a new, unbuilt keyhole-gate payload-release bench mechanism: regenerate the five STEP files byte-identically from `cad/independently_authored/` and run the 26-check independent STEP audit (zero interference over 73 gate positions; coupon released only at 16–20 mm of gate travel).
- File integrity, quote arithmetic, rights screening and cross-repository consistency checks (`scripts/`), all run in CI.

## Scope and limitations
- R01 is bench-only and not validated for flight: material, actuator, end stop, load capacity and retention without power are open.
- The historical aircraft cannot be fully reproduced: frame CAD (D01–D05) is third-party and withheld; the latch and harness were never drawn; flight-controller configurations, mission files, the release command and perception code were not recovered.
- 19/20 is a retrospective composite count without a trial register. No new physical test of any kind was performed.

## Tagging (maintainer step)
The release is prepared on `main` but the tag could not be pushed from the preparation session (HTTP 403). From a clone with write access:

```bash
git fetch origin && git checkout main && git pull --ff-only
python scripts/release_gate.py && python scripts/check_release_lock.py --self-test
git tag -a v1.0.0 -m "SkyRelief v1.0.0" origin/main && git push origin v1.0.0
```

Pushing the tag runs `.github/workflows/release.yml`, which repeats the gates and publishes the GitHub release with the archive and SHA-256 files below.

## Integrity
The release workflow attaches `SkyRelief_Mechanical_Source_Release_v1.0.0.zip` (built with `git archive` from the tagged commit) and its `.sha256`. Per-file SHA-256 values are in `verification/file_manifest.csv`.
