# R01 design analysis: load path, release window and failure modes

**Scope.** Indicative engineering analysis of the unbuilt R01 reference. Every number below either comes from the R01 geometry or is an assumption stated next to it. Nothing here is a rating, and nothing applies to the historical SkyRelief latch.

## 1. Load path

Payload weight *W* acts on the coupon. In the locked state the Ø10 flange bears on the two ledges either side of the 6 mm neck slot. The gate is supported by the base plate (after closing the 0.5 mm running clearance), except over the Ø18 drop window, where it spans as a slotted plate. The rails react only lateral and uplift loads.

| Quantity | Value | Basis |
|---|---|---|
| Flange bearing area on ledges | ≈ 22.4 mm² | Ø10 disc minus a 6 mm strip through its centre (geometry) |
| Gate web beside the slot | 2 × 7.5 mm × 3 mm | (21 − 6)/2 each side, gate thickness 3 |
| Unsupported span under coupon | 18 mm | Drop window diameter |

Example (assumed): a 0.5 kg test mass gives *W* = 4.9 N and a mean ledge bearing pressure of about 0.22 MPa. Whether the gate webs, rails and coupon survive a given load depends on the material and process, which are **unassigned**. No load capacity is claimed.

## 2. Actuation force and torque (indicative)

To release, the actuator must slide the gate against friction at the flange/gate interface and the gate/base interface:

  *F*ₐ ≥ (μ₁ + μ₂) *W* + *F*_spring (if a return spring is added)

With assumed μ₁ = μ₂ = 0.3 and *W* = 4.9 N, *F*ₐ ≈ 2.9 N. A crank of radius *r* sweeping 90° produces a chord of 2*r* sin 45°; covering the 18 mm stroke needs *r* ≈ 12.7 mm, so the torque demand is about 0.037 N·m before any safety factor. An actuator is acceptable only if its **verified** torque at the actual supply voltage exceeds the measured friction torque by a declared factor (suggested ≥ 3). Friction coefficients must be measured on the chosen material pair; the 0.3 values are placeholders.

## 3. Release window (verified geometrically)

`scripts/independent_step_audit.py` lowers the coupon at gate offsets sampled every 0.5 mm. The coupon falls clear **only for offsets of 16.0–20.0 mm**: the Ø10 flange fits through the Ø14 aperture only when the two centres are within 2 mm. Consequences:

- **Drift margin.** The gate can creep up to about 15.5 mm without releasing. That is a large margin against accidental release from small displacements.
- **Over-travel recapture.** Beyond 20 mm the aperture rim catches the flange again; by 24 mm the stem collides with the gate. A hard end stop at 18 mm (±1 mm) is required, or the gate can over-drive and re-retain the load.
- **Endpoint accuracy.** The actuator must place the gate within ±2 mm of 18 mm. Servo endpoints therefore need calibration against the stop, not just a nominal pulse width.

## 4. Power-loss state

R01 has no detent or spring, so an unpowered gate is held only by friction and whatever the actuator's gear train resists. Its behaviour under vibration is **unknown**. A fail-retained design would add a spring biasing the gate toward 0 mm and a stop at 0 mm, so loss of actuator power returns the mechanism to the locked state. That spring adds to *F*ₐ above.

## 5. Tolerance stack (nominal)

| Interface | Nominal clearance | Sensitive to |
|---|---|---|
| Gate–wall, each side | 0.5 mm | Rail straightness, gate width tolerance, swelling of printed parts |
| Gate–base and gate–lip | 0.5 mm each | Plate flatness; gate thickness |
| Stem–neck, each side | 0.5 mm | Stem diameter, slot width |
| Flange–aperture radial | 2.0 mm | Sets the ±2 mm release window |

The 0.5 mm clearances suit FDM printing and light machining; they have not been tolerance-analysed for a specific process.

## 6. Failure modes

| Mode | Effect | Design control (proposed) | Verification still required |
|---|---|---|---|
| Over-travel past 20 mm | Load re-captured; may jam | Hard end stop at 18 mm | Cycle test at the stop |
| Under-travel below 16 mm | No release | Calibrate endpoint to stop | Endpoint repeatability test |
| Gate creep under vibration | Unintended motion (release only after >15.5 mm) | Detent or return spring | Vibration test with dummy load |
| Racking in rails | High friction, stall | Long gate (78 mm) vs 21 mm width helps; lubricate | Measured actuation force |
| Ledge or web fracture | Dropped load | Choose material; size webs | Static proof load to a declared factor |
| Coupon tilt | Binding in neck | Limit off-axis load; chamfers | Off-axis load test |
| Actuator stall | No release; supply sag | Torque margin; supply sizing | Bench current at stall |

## 7. Proposed acceptance criteria (none performed)

1. Retains a declared proof load (e.g. 3× the intended dummy mass) for a declared time without visible deformation.
2. Releases the dummy load in ≥ N consecutive cycles (N declared beforehand) with each event logged.
3. Measured actuation force at the declared load is below one third of the actuator's verified capacity.
4. With actuator power removed, the gate stays locked under a declared vibration exposure.
5. Every test is propeller-free and off-aircraft. **BENCH-ONLY, NOT VALIDATED FOR FLIGHT.**
