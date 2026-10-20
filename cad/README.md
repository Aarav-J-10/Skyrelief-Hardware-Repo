# New CAD and historical exclusions
No historical mechanical CAD passed the redistribution gate; see [manifest](../data/withheld_asset_manifest.csv).
R01 is a new independent bench keyhole gate. Its [Python source](independently_authored/build_reference.py) and [parameter table](independently_authored/parameters.json) never read historical STEP. Install cadquery-ocp==8.0.1.1.0 and run: python cad/independently_authored/build_reference.py

The neutral STEP exports preserve editable solids; Python and JSON preserve source intent. No FreeCAD feature tree, full aircraft or installed latch equivalence is claimed. Material, fabrication tolerance, load rating and actuator linkage remain unassigned. Source parameters are currently a checked design table: changes outside supported invariants require modifying the builder, then repeating verification.
