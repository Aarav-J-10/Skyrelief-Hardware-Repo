"""Vector two-state drawing of the R01 bench reference (plan view and section A-A).
SPDX-FileCopyrightText: 2026 Aarav Jalan and Abhinav Patro
SPDX-License-Identifier: MIT

Drawn from cad/independently_authored/parameters.json with the same placement
rules as build_reference.py; envelopes are cross-checked against
verification/independent_step_audit.json. Writes drawings/R01_two_state.{svg,pdf,png}.
Requires matplotlib==3.11.2.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['svg.hashsalt'] = 'SkyRelief-R01'  # deterministic SVG element ids
from matplotlib.patches import Rectangle, Circle, Polygon

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / 'cad/independently_authored/parameters.json').read_text())
L, W, B, T = P['base_length'], P['base_width'], P['base_thickness'], P['release_travel']
GL, GW, GT, G, GZ = P['gate_length'], P['gate_width'], P['gate_thickness'], P['rail_clearance'], P['gate_bottom_z']
XC, YC = L / 2, W / 2
AP, NECK, FL, ST, WIN = P['gate_release_hole_diameter'], P['gate_neck_width'], P['coupon_flange_diameter'], P['coupon_stem_diameter'], P['drop_window_diameter']
LOW, HIGH = YC - GW / 2 - G - 4, YC + GW / 2 + G
LIPZ = GZ + GT + G
TOP = LIPZ + 2

audit = json.loads((ROOT / 'verification/independent_step_audit.json').read_text())
bb = {f['file']: f['bbox_mm'] for f in audit['files']}
assert abs(bb['R01_chassis.step'][3] - L) < 1e-3 and abs(bb['R01_chassis.step'][5] - TOP) < 1e-3
assert abs(bb['R01_gate.step'][0] - 10) < 1e-3 and abs(bb['R01_gate.step'][2] - GZ) < 1e-3

INK, TEAL, GREY, AMBER = '#1b1b1b', '#1f6f78', '#c9d1d6', '#c98a1b'


def plan(ax, dx, title):
    ax.add_patch(Rectangle((0, 0), L, W, fc='#eef1f3', ec=INK, lw=1.0))
    for x in (6, L - 6):
        for y in (6, W - 6):
            ax.add_patch(Circle((x, y), P['mount_hole_diameter'] / 2, fc='white', ec=INK, lw=0.8))
    for y in (LOW, HIGH):
        ax.add_patch(Rectangle((5, y), L - 10, 4, fc=GREY, ec=INK, lw=0.8))
    ax.add_patch(Circle((XC, YC), WIN / 2, fill=False, ec=INK, lw=0.8, ls=(0, (3, 2))))
    x0 = 10 + dx
    ax.add_patch(Rectangle((x0, YC - GW / 2), GL, GW, fc=TEAL, ec=INK, lw=1.0, alpha=0.9))
    ax.add_patch(Circle((XC - T + dx, YC), AP / 2, fc='white', ec=INK, lw=0.8))
    ax.add_patch(Rectangle((XC - T + dx, YC - NECK / 2), T + 6, NECK, fc='white', ec='none'))
    ax.plot([XC - T + dx + 2.0, XC + 6 + dx], [YC - NECK / 2] * 2, color=INK, lw=0.8)
    ax.plot([XC - T + dx + 2.0, XC + 6 + dx], [YC + NECK / 2] * 2, color=INK, lw=0.8)
    ax.plot([XC + 6 + dx] * 2, [YC - NECK / 2, YC + NECK / 2], color=INK, lw=0.8)
    ax.add_patch(Circle((18 + dx, YC), 1.6, fc='white', ec=INK, lw=0.8))
    for y in (LOW + 4, HIGH - 3):
        ax.add_patch(Rectangle((5, y), L - 10, 3, fc=GREY, ec=INK, lw=0.6, alpha=0.55, hatch='////'))
    ax.add_patch(Circle((XC, YC), FL / 2, fc=AMBER, ec=INK, lw=0.9, alpha=0.95))
    ax.add_patch(Circle((XC, YC), ST / 2, fill=False, ec=INK, lw=0.6))
    ax.annotate('', xy=(10 + dx + GL + 2, YC - GW / 2 - 7), xytext=(10 + GL + 2, YC - GW / 2 - 7),
                arrowprops=dict(arrowstyle='->', lw=1.0, color=INK)) if dx else None
    ax.plot([0, L], [YC, YC], color=INK, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax.text(1, YC + 1, 'A', fontsize=8); ax.text(L - 3, YC + 1, 'A', fontsize=8)
    ax.set_title(title, fontsize=8, loc='left')
    ax.set_xlim(-3, L + 3); ax.set_ylim(-3, W + 3); ax.set_aspect('equal'); ax.axis('off')


def section(ax, dx):
    ax.add_patch(Rectangle((0, 0), XC - WIN / 2, B, fc=GREY, ec=INK, lw=0.8, hatch='////'))
    ax.add_patch(Rectangle((XC + WIN / 2, 0), L - XC - WIN / 2, B, fc=GREY, ec=INK, lw=0.8, hatch='////'))
    x0 = 10 + dx
    segs = [(x0, XC - T + dx - AP / 2), (XC + 6 + dx, x0 + GL)]  # gate material along y = YC (neck + aperture cut)
    for a, b in segs:
        ax.add_patch(Rectangle((a, GZ), b - a, GT, fc=TEAL, ec=INK, lw=0.8, alpha=0.9))
    ax.add_patch(Rectangle((XC - ST / 2, -3), ST, GZ + GT + 3, fc=AMBER, ec=INK, lw=0.8))
    ax.add_patch(Rectangle((XC - FL / 2, GZ + GT), FL, 2, fc=AMBER, ec=INK, lw=0.8))
    ax.add_patch(Circle((18 + dx, GZ + GT / 2), 0.01, fc=INK))
    ax.set_xlim(-3, L + 3); ax.set_ylim(-5, 13); ax.set_aspect('equal'); ax.axis('off')


fig, axs = plt.subplots(2, 2, figsize=(7.2, 4.4), gridspec_kw={'height_ratios': [3.2, 1.0]})
plan(axs[0, 0], 0, '(a) Locked: gate 0 mm; Ø10 flange on 6 mm neck')
plan(axs[0, 1], T, f'(b) Released: gate +{T:g} mm; Ø14 aperture under flange')
section(axs[1, 0], 0); section(axs[1, 1], T)
axs[1, 0].set_title('Section A–A (locked)', fontsize=8, loc='left'); axs[1, 1].set_title('Section A–A (released)', fontsize=8, loc='left')
fig.text(0.5, 0.012, f'R01 new unbuilt bench reference. Base {L:g}×{W:g}×{B:g} mm; gate {GL:g}×{GW:g}×{GT:g} mm; clearance {G:g} mm; '
         f'release window 16–20 mm.\nSection A–A is on the gate centre line (the flange bears on the neck ledges either side of it). '
         f'Material and actuator unassigned.', ha='center', fontsize=6.5)
fig.tight_layout(rect=(0, 0.06, 1, 1))
out = ROOT / 'drawings'
for ext in ('svg', 'pdf'):
    fig.savefig(out / f'R01_two_state.{ext}', metadata={'Date': None} if ext == 'svg' else {'CreationDate': None})
fig.savefig(out / 'R01_two_state.png', dpi=300)
print('wrote drawings/R01_two_state.{svg,pdf,png}')
