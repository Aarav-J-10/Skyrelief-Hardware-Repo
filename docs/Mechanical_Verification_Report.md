# Mechanical verification report

Run on 2026-10-20, Ubuntu 24.04 (x86-64), Python 3.13.16, cadquery-ocp 8.0.1.1.0. The original 0.1.0 exports were produced on Windows with Python 3.12.14 (`verification/tool_versions.json`). CI repeats these steps on Python 3.12.

| Step | Command | Result |
|---|---|---|
| Regenerate R01 | `python cad/independently_authored/build_reference.py` | PASS: 5 STEP files; two runs byte-identical; identical to the 0.1.0 files apart from CRLF line endings |
| Generator self-check | (same) | Valid B-rep, positive volume, correct solid counts; zero chassis/gate overlap at 19 integer positions |
| Independent STEP audit | `python scripts/independent_step_audit.py` | PASS, 26/26 (`verification/independent_step_audit.json`) |
| File checks | `python scripts/validate_repository.py` | See `verification/repository_checks.json` |
| Rights gate | `python scripts/release_gate.py` | No withheld CAD in tree or Git history |
| Release lock | `python scripts/check_release_lock.py --self-test` | Lock matches repository facts; 6 applicable negative tests rejected |

## Independent audit results

| Part | Solids | Volume (mm³) | Envelope (mm) |
|---|---|---|---|
| R01_chassis | 1 | 39 746.07 | 110 × 64 × 11 |
| R01_gate | 1 | 4 118.09 | 78 × 21 × 3 (at x 10–88, z 5.5–8.5) |
| R01_coupon | 1 | 382.88 | Ø10 × 13.5 (z −3 to 10.5) |
| R01_locked_assembly | 3 | 44 247.04 | 110 × 64 × 14 |
| R01_released_assembly | 3 | 44 247.04 | 110 × 64 × 14 |

- Chassis/gate and coupon/gate common volume: zero (below 10⁻⁶ mm³) at all 73 gate positions from 0 to 18 mm in 0.25 mm steps.
- Locked: the coupon touches the gate within the first 0.5 mm of descent.
- Released (+18 mm): the coupon descends 25 mm without touching gate or chassis.
- Release window (0.5 mm sampling, 0–23 mm): falls clear only at 16.0–20.0 mm; retained below 16 mm; re-captured above 20 mm; stem collides with the gate from about 23–24 mm.

## What this does not demonstrate

Clearance between samples, behaviour of a fabricated part, friction, wear, deflection, load capacity, actuator torque, retention with power removed or under vibration, and anything about flight. No physical test of any kind was performed.
