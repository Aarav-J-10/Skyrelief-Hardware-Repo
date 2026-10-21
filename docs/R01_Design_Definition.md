# R01 keyhole-gate bench reference — design definition

**Release state: DIGITALLY REPRODUCIBLE REFERENCE (`N`, new and unbuilt).** R01 was written in 2026, after the SkyRelief aircraft were flown. It is not the historical latch, it was never fitted to either aircraft, and none of its geometry is taken from the withheld D01–D05 STEP files. The generator (`cad/independently_authored/build_reference.py`) imports only Open CASCADE primitives and `parameters.json`; it opens no external CAD file.

## Purpose

The historical Delivery UAV used a servo to withdraw a retaining rod (photograph `pld20`). Its dimensions, linkage and supply were never recorded, and the only recovered servo-named CAD (D05) is a fixed bracket. R01 gives a reviewer a small, fully specified mechanism they can regenerate, inspect and, if they choose, fabricate as a bench study of the *retain → actuate → release* principle. It does not reproduce the historical part.

## Concept

A sliding gate rides in two rails on a base plate. A payload coupon (a stem with a flange) hangs through a narrow neck slot in the gate. The flange is wider than the neck, so in the **locked** state the coupon rests on the gate. Sliding the gate by the release travel brings a larger aperture under the coupon; the flange passes through the aperture and the base drop window, and the coupon falls.

| State | Gate position | Coupon |
|---|---|---|
| Locked | x offset 0 mm | Flange (Ø10) bears on the 6 mm neck ledges |
| Released | x offset +18 mm | Flange centred over the Ø14 aperture; free to fall through the Ø18 window |

## Coordinate frame and nominal geometry (mm)

Origin at the base plate's lower-left corner; +x along gate travel, +z up. Values are from `parameters.json` and were re-measured from the exported STEP files by `scripts/independent_step_audit.py`.

| Feature | Value | Notes |
|---|---|---|
| Base plate | 110 × 64 × 5 | Four Ø3.4 mount holes on a 98 × 52 pattern, 6 mm from edges |
| Drop window | Ø18 through base at (55, 32) | Coupon centre line |
| Rails | Walls y 17–21 and 43–47; lips y 21–24 and 40–43 at z 9–11 | Run x 5–105; overall chassis height 11 |
| Gate | 78 × 21 × 3 at z 5.5–8.5 | 0.5 mm clearance below (base), above (lips) and to each wall |
| Release aperture | Ø14 at x = 37 (locked frame) | Moves to x = 55 after 18 mm travel |
| Neck slot | 6 mm wide, from aperture to x = 61 | Stem passes with 0.5 mm per side |
| Actuator interface hole | Ø3.2 at (18, 32) in the gate | Linkage attachment point; **no actuator is specified** |
| Coupon | Stem Ø5, z −3 to 8.5; flange Ø10 × 2, z 8.5–10.5 | Coupon is a test article, not a payload interface |

## Degrees of freedom

One intended degree of freedom: gate translation in +x, constrained laterally by the walls and vertically by the base and lips. The coupon is free in z once released. Nothing in R01 limits gate travel; end stops, a return spring and a detent are open design items (see [Design analysis](Design_Analysis.md)).

## Deliberately absent

Servo body, horn, pushrod or crank, end stops, detent, return spring, fasteners, material, print/machining process, tolerances beyond the nominal 0.5 mm clearances, and any mounting interface to an aircraft. Each is listed with an acceptance criterion in [Design analysis](Design_Analysis.md).

## Files

| File | Role |
|---|---|
| `cad/independently_authored/parameters.json` | Editable parameters |
| `cad/independently_authored/build_reference.py` | Native generator (source of truth) |
| `cad/independently_authored/exports/R01_*.step` | Five exports: chassis, gate, coupon, locked assembly, released assembly |
| `cad/independently_authored/geometry_verification.json` | Generator self-check |
| `verification/independent_step_audit.json` | Independent re-import audit |
| `drawings/R01_dimensioned_reference.{pdf,svg}`, `drawings/R01_geometry_preview.png` | Human-readable views |
| `bom/reference_R01_bom.csv` | Part list (materials unassigned) |
