"""Independent audit of the five released R01 STEP files.
SPDX-FileCopyrightText: 2026 Aarav Jalan and Abhinav Patro
SPDX-License-Identifier: MIT

Reads only the exported STEP files (never the generator's in-memory shapes) and
checks: B-rep validity, solid counts, volumes, bounding boxes, a fine 0.25 mm
chassis/gate and coupon/gate interference sweep, and a coupon drop-path test in
the locked and released states. Geometry only: no material, load, friction,
servo, linkage or flight property is evaluated.
Requires cadquery-ocp==8.0.1.1.0. Run from the repository root.
"""
import hashlib, json, sys
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.gp import gp_Trsf, gp_Vec
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / 'cad/independently_authored/exports'
TOL = 1e-6  # mm^3, numerical zero for common volume


def read(name):
    r = STEPControl_Reader()
    assert r.ReadFile(str(EXP / name)) == IFSelect_RetDone, name
    assert r.TransferRoots() > 0, name
    return r.OneShape()


def vol(s):
    p = GProp_GProps(); BRepGProp.VolumeProperties_s(s, p); return p.Mass()


def nsolids(s):
    e = TopExp_Explorer(s, TopAbs_SOLID); n = 0
    while e.More():
        n += 1; e.Next()
    return n


def bbox(s):
    b = Bnd_Box(); b.SetGap(0.0); BRepBndLib.Add_s(s, b, False)
    mn, mx = b.CornerMin(), b.CornerMax()
    x0, y0, z0, x1, y1, z1 = mn.X(), mn.Y(), mn.Z(), mx.X(), mx.Y(), mx.Z()
    return [round(v, 3) for v in (x0, y0, z0, x1, y1, z1)]


def move(s, dx=0.0, dz=0.0):
    t = gp_Trsf(); t.SetTranslation(gp_Vec(dx, 0, dz))
    return BRepBuilderAPI_Transform(s, t, True).Shape()


def common(a, b):
    return abs(vol(BRepAlgoAPI_Common(a, b).Shape()))


def main():
    params = json.loads((ROOT / 'cad/independently_authored/parameters.json').read_text())
    reported = json.loads((ROOT / 'cad/independently_authored/geometry_verification.json').read_text())
    rep_vol = {x['file']: x['volume_mm3'] for x in reported['part_exports']}
    travel = float(params['release_travel'])
    checks, fails = [], []

    def check(name, ok, detail=None):
        checks.append({'check': name, 'pass': bool(ok), 'detail': detail})
        if not ok:
            fails.append(name)

    shapes, files = {}, []
    for f in sorted(EXP.glob('*.step')):
        s = read(f.name); shapes[f.stem] = s
        v = vol(s); expect = 3 if 'assembly' in f.stem else 1
        files.append({'file': f.name, 'sha256_lf_bytes': hashlib.sha256(f.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                      'solids': nsolids(s), 'volume_mm3': round(v, 6), 'bbox_mm': bbox(s)})
        check('B-rep valid: ' + f.name, BRepCheck_Analyzer(s).IsValid())
        check('Solid count: ' + f.name, nsolids(s) == expect, nsolids(s))
        check('Volume matches reported: ' + f.name, abs(v - rep_vol[f.name]) < 1e-6 * max(1, v), [v, rep_vol[f.name]])
    check('Five STEP files present', len(files) == 5, [x['file'] for x in files])

    ch, gate, cp = shapes['R01_chassis'], shapes['R01_gate'], shapes['R01_coupon']
    b = bbox(ch)
    check('Chassis envelope equals parameters (L x W)',
          abs(b[3] - b[0] - params['base_length']) < 1e-3 and abs(b[4] - b[1] - params['base_width']) < 1e-3, b)
    g = bbox(gate)
    check('Gate envelope equals parameters', abs(g[3] - g[0] - params['gate_length']) < 1e-3
          and abs(g[4] - g[1] - params['gate_width']) < 1e-3 and abs(g[5] - g[2] - params['gate_thickness']) < 1e-3, g)
    check('Assemblies sum part volumes', abs(vol(shapes['R01_locked_assembly']) - (vol(ch) + vol(gate) + vol(cp))) < 1e-3)
    check('Released assembly volume equals locked', abs(vol(shapes['R01_released_assembly']) - vol(shapes['R01_locked_assembly'])) < 1e-3)

    sweep = []
    steps = int(travel / 0.25)
    for i in range(steps + 1):
        dx = i * 0.25; gm = move(gate, dx)
        sweep.append({'dx_mm': dx, 'chassis_gate_mm3': common(ch, gm), 'coupon_gate_mm3': common(cp, gm)})
    check('Chassis/gate zero interference over 0.25 mm sweep', all(x['chassis_gate_mm3'] < TOL for x in sweep), len(sweep))
    check('Coupon/gate zero interference over 0.25 mm sweep', all(x['coupon_gate_mm3'] < TOL for x in sweep), len(sweep))

    # Drop path: lower the coupon in 0.5 mm steps up to 25 mm.
    def blocked(gate_dx):
        gm = move(gate, gate_dx)
        for k in range(1, 51):
            dz = -0.5 * k
            c = move(cp, dz=dz)
            if common(c, gm) > TOL or common(c, ch) > TOL:
                return dz
        return None
    lock_block = blocked(0.0)
    rel_block = blocked(travel)
    check('Locked state: flange blocked by gate within first 1 mm of descent', lock_block is not None and lock_block >= -1.0, lock_block)
    check('Released state: coupon descends 25 mm with no gate/chassis contact', rel_block is None, rel_block)

    # Release window: gate offsets (0.5 mm steps, 0-23 mm) at which the coupon falls clear.
    window = []
    for i in range(0, 47):
        dx = i * 0.5
        if common(cp, move(gate, dx)) > TOL:
            window.append({'dx_mm': dx, 'state': 'stem_interference'})
        else:
            window.append({'dx_mm': dx, 'state': 'falls_clear' if blocked(dx) is None else 'retained'})
    clear = [x['dx_mm'] for x in window if x['state'] == 'falls_clear']
    check('Release window is 16-20 mm of gate travel (0.5 mm sampling)', clear and min(clear) == 16.0 and max(clear) == 20.0
          and clear == [16.0 + 0.5 * j for j in range(9)], clear)
    check('Retained for every sampled offset below 16 mm', all(x['state'] == 'retained' for x in window if x['dx_mm'] < 16), None)

    out = {'scope': 'Independent STEP re-import audit; geometry only; not physical validation',
           'kernel': 'cadquery-ocp 8.0.1.1.0 (Open CASCADE)',
           'files': files, 'sweep_step_mm': 0.25, 'sweep_positions': len(sweep),
           'max_chassis_gate_common_mm3': max(x['chassis_gate_mm3'] for x in sweep),
           'max_coupon_gate_common_mm3': max(x['coupon_gate_mm3'] for x in sweep),
           'locked_first_contact_dz_mm': lock_block, 'released_first_contact_dz_mm': rel_block,
           'release_window_mm': [min(clear), max(clear)] if clear else None, 'release_window_samples': window,
           'checks_run': len(checks), 'failures': fails, 'status': 'PASS' if not fails else 'FAIL', 'checks': checks,
           'not_demonstrated': ['continuous (between-sample) clearance', 'friction, wear, deflection', 'load capacity',
                                'servo torque or linkage', 'unpowered retention under vibration', 'flight use']}
    (ROOT / 'verification/independent_step_audit.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: out[k] for k in ('status', 'checks_run', 'sweep_positions', 'locked_first_contact_dz_mm', 'released_first_contact_dz_mm')}))
    if fails:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
