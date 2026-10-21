# Mechanical system architecture

Two separate aircraft were built in 2024–2025. A third mechanical item, R01, was designed in 2026 and has never been built.

| Item | Role | Release state | Evidence |
|---|---|---|---|
| **Delivery UAV** | Carries and releases the payload | Functionally described historical subsystem | Component list, photos `pld25`, `pld13`, `pld10`, `pld2`, `pld20`; Vivo Ignite build steps |
| **Scout UAV** | Manually piloted FPV reconnaissance; carries no payload | Functionally described historical subsystem | Component list, photos `sc9`, `sc7`, `sc8`; build steps |
| **Historical release mechanism** | Servo withdraws a retaining rod; payload falls | Functionally described historical subsystem | Photo `pld20` (MG90S marking, wooden support) |
| D01–D05 STEP files | F450 plates, frame assembly, arm, fixed servo support | **Unresolved / not release-cleared** (withheld) | Private audit metrics only; see [rights disposition](Source_Rights_Disposition.md) |
| **R01 bench gate** | Independent study of retain/actuate/release | Digitally reproducible reference (new, unbuilt) | Generator, STEP exports, audits in this repository |

## Delivery UAV

An F450-class quadrotor: power distribution board, four arms, top plate, landing gear. The build text lists four 2212 920 KV-family motors on M3 × 10 mm screws with 0.8 mm washers, 30 A-labelled ESCs soldered to the PDB, 10 × 4.5 propellers, and an avionics stack (Pixhawk 2.4.8, NEO-M8N GPS/compass, FS-iA6B receiver, 3DR telemetry, safety switch, buzzer) on the top plate. A UBEC from the PDB feeds an FPV assembly. The retaining mechanism hangs below the frame (`pld20`). Mass and centre-of-gravity records do not survive; the listed part masses are not a weighed aircraft.

## Scout UAV

A small carbon-fibre frame with a GHF411 PRO-BMI 40 A F4 2–6S all-in-one controller, four FT Gremlin 1104 5400 KV motors on M2 × 6 mm screws, an R81 receiver and an FPV camera/VTX. The final propeller set (HQ 2.5 × 3 or 2.5 × 2.5 × 3) and battery cell count are unresolved.

## Where R01 fits

R01 is a stand-alone bench mechanism. It has M3 clearance holes on a 98 × 52 mm pattern but **no defined interface to either aircraft**, and it has not been checked against the F450 frame. It should be read as a reproducible example of the release principle, not as a replacement part.

## What a reader can and cannot rebuild

| Question | Answer |
|---|---|
| What can I rebuild from these files today? | R01 (geometry only; material and actuator are yours to choose and qualify). |
| What remains inferred? | Frame fastener map, latch dimensions, mounting of the historical mechanism. |
| What was actually flown? | The two historical aircraft and their wooden/servo latch, per author reports and photographs. |
| What is only simulated? | Nothing mechanical; the mission models live in the separate computational supplement. |
