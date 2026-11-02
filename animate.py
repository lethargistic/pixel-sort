"""
arg example:
python animate.py sort/mesmind.webp -o frames -n 240 -i random -c 0:500 -a -90 --fps 24 --video out.gif
"""
import argparse
import random
from pathlib import Path

import imageio.v3 as iio
import numpy as np
from PIL import Image
from pixelsort import pixelsort

NUMERIC = {"-c": "char_length", "-a": "angle", "-t": "lower_threshold",
           "-u": "upper_threshold", "-r": "randomness"}


def span(s):
    a1, _, b = s.partition(":")
    return float(a1), float(b or a1)


p = argparse.ArgumentParser()
p.add_argument("image")
p.add_argument("-o", "--out", default="frames", help="frames folder")
p.add_argument("-n", "--frames", type=int, default=30)
p.add_argument("--fps", type=float, default=24)
p.add_argument("--video", help="compile to this .gif/.mp4")
p.add_argument("--seed", type=int, default=0,
               help="same seed every frame = stable intervals (no flicker)")
p.add_argument("-i", dest="interval_function")
p.add_argument("-s", dest="sorting_function")
for flag, name in NUMERIC.items():
    p.add_argument(flag, dest=name, type=span)
a = p.parse_args()

fixed = {k: v for k in ("interval_function", "sorting_function") if (v := getattr(a, k))}
sweep = {k: np.linspace(*v, a.frames) for k in NUMERIC.values() if (v := getattr(a, k))}

img = Image.open(a.image)
out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)

frames = []
for i in range(a.frames):
    random.seed(a.seed)
    params = {k: float(v[i]) for k, v in sweep.items()}
    c = NUMERIC["-c"]
    if c in params:
        params[c] = max(2.0, params[c])
    print(f"{i + 1}/{a.frames}", params, flush=True)
    frame = pixelsort(img, **fixed, **params).convert("RGB")
    frame.save(out / f"frame_{i:04d}.png")
    frames.append(np.asarray(frame))

if a.video:
    opts = {"duration": 1000 / a.fps, "loop": 0} if a.video.endswith(".gif") else {"fps": a.fps}
    iio.imwrite(a.video, frames, **opts)
    print("wrote", a.video)
