# Assembly instructions

Two separate procedures. Part A records how the historical Delivery and Scout UAVs were reported to be assembled; it is a documentary account, not a verified recipe. Part B is a complete procedure for the R01 bench reference. **Neither part is a flight-qualification procedure.**

## Part A — Historical frame integration (documented, not verified)

Source: Vivo Ignite build section (author-supplied PDF), component lists in `evidence/original/`, photographs in `images/`. Steps marked **GAP** cannot be completed from surviving records.

### Delivery UAV (F450-class)

1. Solder four ESCs and the power module to the PDB (bottom plate). **GAP:** connector type, wire gauge, power-module insertion point.
2. Attach the frame arms ("legs") to the PDB plate. **GAP:** screw schedule for plate–arm joints (the withheld D02 model names 16 M3 × 12 and 8 M3 × 5 screws, which is a CAD label, not a record of the build).
3. Attach each motor to its arm with M3 × 10 mm screws and 0.8 mm M3 washers (source text: 4 screws, 3 washers per motor). **GAP:** thread engagement, winding clearance, threadlocker.
4. Fit the top plate and mount the avionics: Pixhawk 2.4.8, NEO-M8N GPS mast, FS-iA6B receiver, buzzer, safety switch, 3DR telemetry air module (`pld13`, `pld10`). Gel tape, damping pads and zip ties are reported. **GAP:** controller orientation, mast height.
5. Solder the UBEC input to the PDB and feed the FPV assembly from its output.
6. Connect each ESC's 3-pin header to Pixhawk outputs OUT1–OUT4 (source step 8). **GAP:** which motor on which output, ESC protocol.
7. Fit 10 × 4.5 propellers in the correct rotation only after a propeller-free motor-direction check; swap two phase leads to reverse a motor.
8. Mount the retaining mechanism under the frame (`pld20`). **GAP:** dimensions, attachment, servo connection and supply.

### Scout UAV

1. Mount the GHF411 AIO in the centre of the carbon frame on damping pads.
2. Fit four FT Gremlin 1104 motors with M2 × 6 mm screws and washers; solder leads to the AIO ESC pads in the intended rotation.
3. Install the R81 receiver, bind to the Zorro transmitter, and secure with hook-and-loop or heat-shrink.
4. Add the FPV camera/VTX powered from a 5 V regulated output; route antennas away from power leads.
5. Fit propellers by rotation direction. **GAP:** final propeller set.
6. Connect a 2–4S LiPo through XT30. **GAP:** cell count actually flown (an 1100 mAh capacity is reported).

## Part B — R01 bench reference (complete within its scope)

**Tools:** printer or mill capable of ±0.1 mm; M3 hardware for mounting; calipers.

1. **Generate** the files: `pip install -r requirements-cad.txt && python cad/independently_authored/build_reference.py`. Confirm the console prints `PASS digital geometry only`.
2. **Audit** them: `python scripts/independent_step_audit.py` should print `"status": "PASS"`.
3. **Choose and record a material and process** for chassis, gate and coupon. The repository does not assign one. Record it in a copy of `bom/reference_R01_bom.csv`.
4. **Fabricate** `R01_chassis.step`, `R01_gate.step`, `R01_coupon.step`. Measure gate width (21.0 mm nominal) and rail gap (22.0 mm nominal); sand or adjust until the gate slides by hand without play greater than the 0.5 mm design clearance.
5. **Insert the gate** from the open end of the rails with the Ø14 aperture toward x = 0 (the actuator hole toward the near end).
6. **Load the coupon**: with the gate at 0 mm, drop the stem through the neck slot and drop window so the flange rests on the gate.
7. **Add an end stop** at 18 mm of travel (see [design analysis §3](Design_Analysis.md)); without it the gate can over-travel and re-capture the coupon.
8. **Manual check**: slide the gate by hand. The coupon must stay retained up to about 15.5 mm and fall between 16 and 20 mm.
9. **Actuator (optional, user-specified)**: attach a linkage to the Ø3.2 hole at x = 18 mm. Size it per [design analysis §2](Design_Analysis.md). Any servo, supply and control source are your design and must be documented separately.

Mark the assembled unit **BENCH-ONLY, NOT VALIDATED FOR FLIGHT.**
