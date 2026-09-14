#!/usr/bin/env python3
"""
strip_rim_v2.py — Code-layer QC pass for layered-stamp-skill.

Target: the thin pale rim / white outline that ImageGen tends to draw
around dark shapes (dog, child, ladder). We detect only pixels that are:

  1. bright and gray-ish (the rim is usually whiter than the warm paper)
  2. within a few pixels of dark ink (so we do not touch the outer paper margin)

Then we replace those pixels with the local median of non-rim neighbors.
"""
import sys
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation


def strip_rim(input_path, output_path,
              bright_min=230,
              rb_max=15,
              dark_max_lum=100,
              dark_dilate=5,
              window=7,
              verbose=True):
    im = Image.open(input_path).convert('RGB')
    arr = np.array(im).astype(np.float64)
    h, w, _ = arr.shape

    lum = arr.mean(axis=2)
    rb = arr[..., 0].astype(np.int16) - arr[..., 2].astype(np.int16)

    # Candidate rim: bright (whiter than warm paper) and low warmness
    rim = (lum > bright_min) & (rb < rb_max)

    # Only keep candidates that are next to dark ink (not outer margin)
    dark = lum < dark_max_lum
    dark_near = binary_dilation(dark, iterations=dark_dilate)
    rim = rim & dark_near

    out = arr.copy()
    ys, xs = np.where(rim)
    for y, x in zip(ys, xs):
        y0 = max(0, y - window)
        y1 = min(h, y + window + 1)
        x0 = max(0, x - window)
        x1 = min(w, x + window + 1)
        patch = arr[y0:y1, x0:x1]
        patch_rim = rim[y0:y1, x0:x1]
        non = patch[~patch_rim]
        if non.shape[0] >= 3:
            out[y, x] = np.median(non, axis=0)
        else:
            # fall back: replace with paper-ish neutral warm tone
            out[y, x] = np.array([232, 220, 200])

    Image.fromarray(out.astype(np.uint8)).save(output_path)
    if verbose:
        print(f'rim pixels cleaned: {rim.sum()}', file=sys.stderr)
    return out


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: strip_rim_v2.py <input.png> <output.png>', file=sys.stderr)
        sys.exit(2)
    strip_rim(sys.argv[1], sys.argv[2])