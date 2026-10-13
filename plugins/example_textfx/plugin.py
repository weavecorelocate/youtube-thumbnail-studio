"""Example extension: heavy outline + glow text effect."""
from __future__ import annotations

from PIL import ImageFilter

from youtube_thumbnail_studio.models.plugin import PluginKind, PluginMeta, Stage


class TextFxPlugin:
    meta = PluginMeta(
        name="ext.textfx",
        version="0.3.1",
        kind=PluginKind.EFFECT,
        stage=Stage.POST,
        priority=150,
        summary="Applies glow and heavy outline to the composed text layer.",
    )

    def apply(self, ctx):
        if not ctx.canvas.layers:
            return ctx.canvas
        top = ctx.canvas.layers[-1]
        glow = top.filter(ImageFilter.GaussianBlur(12))
        ctx.canvas.layers[-1] = Image.alpha_composite(glow, top)
        return ctx.canvas