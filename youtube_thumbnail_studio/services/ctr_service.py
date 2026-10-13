"""CTRService — heuristic salience score for A/B ranking of candidates."""
from __future__ import annotations

import numpy as np
from PIL import Image


def _contrast_map(img: Image.Image) -> np.ndarray:
    gray = np.asarray(img.convert("L"), dtype=np.float32) / 255.0
    gx = np.abs(np.diff(gray, axis=1, prepend=gray[:, :1]))
    gy = np.abs(np.diff(gray, axis=0, prepend=gray[:1, :]))
    return np.sqrt(gx**2 + gy**2)


def salience_score(img: Image.Image) -> float:
    """0.0-1.0 heuristic. Not a model — a fast triage for ordering variants."""
    edges = _contrast_map(img)
    center = edges[180:540, 320:960]
    edge_energy = float(center.mean())
    saturation = float(np.asarray(img.convert("HSV"))[:, :, 1].mean() / 255.0)
    return round(min(1.0, 0.6 * edge_energy * 4 + 0.4 * saturation), 4)