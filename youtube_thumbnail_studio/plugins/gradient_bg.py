"""Built-in: procedural gradient background source."""
from __future__ import annotations

import numpy as np
from PIL import Image

from youtube_thumbnail_studio.models.plugin import PluginKind, PluginMeta, Stage


class GradientBackground:
    meta = PluginMeta(
        name="builtin.gradient_bg",
        version="1.0.0",
        kind=PluginKind.SOURCE,
        stage=Stage.LOAD,
        priority=10,
        summary="Radial gradient background source.",
    )

    def apply(self, ctx) -> "object":
        w, h = ctx.canvas.width, ctx.canvas.height
        yy, xx = np.mgrid[0:h, 0:w]
        cx, cy = w * 0.5, h * 0.55
        r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        r = r / r.max()
        top = np.array([28, 32, 48], dtype=np.float32)
        bottom = np.array([8, 8, 12], dtype=np.float32)
        blend = r[..., None]
        rgb = (top * (1 - blend) + bottom * blend).astype(np.uint8)
        ctx.canvas.push(Image.fromarray(rgb, "RGB"))
        return ctx.canvas