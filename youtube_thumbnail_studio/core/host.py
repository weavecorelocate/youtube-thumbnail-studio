"""PluginHost — owns the registry, dispatches render stages to extensions."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from PIL import Image

from youtube_thumbnail_studio.config.settings import StudioSettings
from youtube_thumbnail_studio.core.registry import PluginRegistry
from youtube_thumbnail_studio.models.canvas import Canvas
from youtube_thumbnail_studio.models.plugin import Stage

log = logging.getLogger("ytthumb.host")


@dataclass(slots=True)
class HostContext:
    settings: StudioSettings
    stage: Stage
    canvas: Canvas


class PluginHost:
    """Runs the render pipeline: load -> compose -> post-process -> encode."""

    def __init__(self, registry: PluginRegistry, settings: StudioSettings) -> None:
        self.registry = registry
        self.settings = settings

    def run_stage(self, stage: Stage, canvas: Canvas) -> Canvas:
        ctx = HostContext(settings=self.settings, stage=stage, canvas=canvas)
        for plugin in self.registry.for_stage(stage):
            log.debug("stage=%s plugin=%s", stage.value, plugin.meta.name)
            try:
                ctx.canvas = plugin.apply(ctx)
            except Exception:  # noqa: BLE001 — a plugin must not kill the host
                log.exception("plugin %s failed at stage %s", plugin.meta.name, stage.value)
        return ctx.canvas

    def pipeline(self) -> Iterable[Stage]:
        return (Stage.LOAD, Stage.COMPOSE, Stage.POST, Stage.ENCODE)

    def render(self, canvas: Canvas) -> Image.Image:
        for stage in self.pipeline():
            canvas = self.run_stage(stage, canvas)
        return canvas.flatten()