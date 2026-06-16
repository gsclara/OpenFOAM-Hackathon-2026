#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from snapshot_io import parse_input_parameters, list_snapshots, read_snapshot


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--params', default='input_parameters')
    p.add_argument('--fields', default='fields')
    p.add_argument('--step',   type=int, default=None)
    p.add_argument('--out',    default='postProcessing')
    return p.parse_args()


def slice_and_plot(snap, field_names, out_dir):
    xm, ym, zm = snap['xm'], snap['ym'], snap['zm']
    ix = len(xm) // 2
    iy = len(ym) // 2
    iz = len(zm) // 2

    axes_info = [
        ('x_normal', (zm, ym, 'z', 'y'), lambda f: f[ix, :, :]),
        ('y_normal', (xm, zm, 'x', 'z'), lambda f: f[:, iy, :].T),
        ('z_normal', (xm, ym, 'x', 'y'), lambda f: f[:, :, iz].T),
    ]

    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for name in field_names:
        field = snap[name]
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        fig.suptitle(name)

        for ax, (label, (h_coords, v_coords, h_label, v_label), slicer) in zip(axes, axes_info):
            data = slicer(field)
            H, V = np.meshgrid(h_coords, v_coords)
            pc = ax.pcolormesh(H, V, data, shading='auto', cmap='RdBu_r')
            fig.colorbar(pc, ax=ax, shrink=0.8)
            ax.set_xlabel(h_label)
            ax.set_ylabel(v_label)
            ax.set_title(label)
            ax.set_aspect('equal')

        fig.tight_layout()
        fpath = Path(out_dir) / f'{name}_slices.png'
        fig.savefig(fpath, dpi=150)
        plt.close(fig)
        print(f'  saved {fpath}')


def main():
    args = parse_args()

    prm           = parse_input_parameters(args.params)
    sgs_model     = int(prm.get('sgs_model',    0))
    sediment_flag = int(prm.get('sediment_flag', 0))
    fileout       = str(prm.get('fileout',       'channel_test'))

    snaps = list_snapshots(args.fields, fileout)
    if not snaps:
        sys.exit(f'No snapshots found in {args.fields!r} with prefix {fileout!r}')

    if args.step is not None:
        matches = [(s, p) for s, p in snaps if s == args.step]
        if not matches:
            sys.exit(f'Step {args.step} not found')
        step, fpath = matches[0]
    else:
        step, fpath = snaps[-1]

    print(f'Loading step {step}: {fpath}')
    snap = read_snapshot(fpath, sgs_model=sgs_model, sediment_flag=sediment_flag)

    field_names = ['U', 'V', 'W', 'P']
    if 'C'    in snap: field_names.append('C')
    if 'nu_t' in snap: field_names.append('nu_t')

    slice_and_plot(snap, field_names, args.out)


if __name__ == '__main__':
    main()
