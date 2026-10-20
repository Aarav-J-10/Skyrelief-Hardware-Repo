# Assembly and inspection guide

**Historical SkyRelief hardware dossier with modern engineering reconstruction.** Source-supported components and connectivity are distinguished from new reference implementations. Unrecovered pin assignments, firmware parameters and code must not be treated as as-built records or electrically validated flight instructions.

## Historical identification
Use pld25 for the Delivery UAV, pld10 for GPS/controller placement, pld13 for the avionics stack and pld20 for the latch region. Scout sc9 shows the smaller guarded aircraft; sc7/sc8 show its board. These are observed placements, not dimensioned installation drawings.

## Recommended general build sequence
1. Identify exact frame revision and inspect plate/arm damage. Mark forward/up for any new build; STEP axes are export axes.
2. Dry-assemble the two-plate/four-arm structure. Match actual joints to the manufacturer fastener schedule. Resolve screw-length/count contradictions before selecting hardware. No screw grade or torque is supplied.
3. Match motor hole patterns and screw engagement; prevent contact with windings. Resolve motor order/rotation against the actual controller and chosen firmware, with propellers removed.
4. Provide a verified controller orientation and vibration-isolating mount. Route high-current loops away from compass/receiver. The historical GPS mast is visible but no calibrated interference survey exists.
5. Restrain the actual battery and fit landing gear clear of payload/propeller disks. Listed masses do not establish balance or structural margins. Determine centre of gravity independently.
6. Mount a reviewed payload mechanism with clearance from gear, wiring and propellers. R01 has no aircraft mounting qualification.
7. Inspect engagement, strain relief and moving clearance. Any electrical review remains propeller-free; refitting propellers belongs to a separate complete aircraft qualification process.

## R01 digital assembly
Open the locked and released assembly STEP files or regenerate them from Python. Units are mm; XY is the base plane, +Z upward and gate travel is +X 18 mm. The coupon stem is 5 mm and flange 10 mm; the chassis drop opening is 18 mm. No physical assembly trial or fabrication tolerance is implied. An actuator would require a separately engineered linkage, stops and travel review.
