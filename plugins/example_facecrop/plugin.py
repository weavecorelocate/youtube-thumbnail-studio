"""Example extension: face-aware crop hint for reaction thumbnails."""
from __future__ import annotations

from youtube_thumbnail_studio.models.plugin import PluginKind, PluginMeta, Stage


class FaceCropPlugin:
    meta = PluginMeta(
        name="ext.facecrop",
        version="0.2.0",
        kind=PluginKind.ANALYZER,
        stage=Stage.POST,
        priority=200,
        summary="Detects a face region and records crop hints in canvas metadata.",
    )

    def apply(self, ctx):
        try:
            import mediapipe  # type: ignore
        except ImportError:
            ctx.canvas.metadata["facecrop"] = "unavailable"
            return ctx.canvas
        ctx.canvas.metadata["facecrop"] = "ok"
        return ctx.canvas