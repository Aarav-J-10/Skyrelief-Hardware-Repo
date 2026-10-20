# R01 generator, parameters and regeneration

## Dependencies

| Item | Version used for the recorded outputs |
|---|---|
| Python | 3.12 (original export); re-run on 3.13.16 on 2026-10-20 |
| cadquery-ocp (Open CASCADE bindings) | 8.0.1.1.0 (`requirements-cad.txt`) |
| OS | Linux x86-64 (re-run); original platform recorded in `verification/tool_versions.json` |

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-cad.txt
python cad/independently_authored/build_reference.py   # writes 5 STEP files + geometry_verification.json
python scripts/independent_step_audit.py               # re-imports the STEP files and checks them
python scripts/validate_repository.py                  # file, link, hash and BOM checks
```

## Determinism

The generator overwrites the STEP header timestamp with a fixed value, so repeated runs give identical bytes. On 2026-10-20 the five STEP files and `geometry_verification.json` were regenerated twice in a clean copy; both runs were byte-identical to each other and, after normalising line endings, to the committed files. The committed copies carry CRLF line endings introduced by the GitHub web upload; `.gitattributes` now marks STEP files as binary so Git does not alter them further.

## Parameters

Only the parameters below are read. The generator asserts the listed constraints and stops if they fail; the ranges in the last column are the **geometric** consistency conditions in the code, not validated mechanical ranges.

| Key | Nominal | Effect | Geometric condition enforced |
|---|---|---|---|
| `base_length`, `base_width`, `base_thickness` | 110, 64, 5 | Plate envelope | length ≥ 10 + gate_length + travel; width > gate_width + 12 |
| `release_travel` | 18 | Gate stroke and aperture offset | integer; aperture clear of actuator hole |
| `gate_length`, `gate_width`, `gate_thickness` | 78, 21, 3 | Gate envelope | — |
| `gate_bottom_z` | 5.5 | Gate seat height | must equal base_thickness + rail_clearance |
| `rail_clearance` | 0.5 | Running clearance on all sides | > 0 |
| `gate_release_hole_diameter` | 14 | Release aperture | stem < neck < flange < aperture < drop window |
| `gate_neck_width` | 6 | Retention slot | as above |
| `coupon_stem_diameter`, `coupon_flange_diameter` | 5, 10 | Test coupon | as above |
| `drop_window_diameter` | 18 | Base window | as above |
| `mount_hole_diameter` | 3.4 | M3 clearance holes | — |

`material` and `actuator` are informational strings (`UNASSIGNED`, `UNSPECIFIED`). Changing a parameter produces a new design; record it as R02 or later rather than overwriting R01.

## What the checks establish

- Generator: each part is a valid B-rep with positive volume; each STEP file re-reads to the right number of solids; chassis and gate share zero volume at 19 integer gate positions (0–18 mm).
- Independent audit (`scripts/independent_step_audit.py`, reads only the STEP files): 26 checks, including envelopes against `parameters.json`, zero chassis/gate and coupon/gate common volume at 73 positions in 0.25 mm steps, contact within the first 0.5 mm of coupon descent when locked, 25 mm of contact-free descent when released, and a release window: sampled every 0.5 mm, the coupon falls clear only for gate offsets of 16–20 mm.

These are statements about the digital solids. They do not test continuous clearance between samples, friction, wear, deflection, load capacity, actuator torque, retention under vibration or anything in flight.
