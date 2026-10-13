"""RenderService — turns a validated Spec into a finished thumbnail file."""
from __future__ import annotations

import logging
from pathlib import Path

from youtube_thumbnail_studio.core.host import PluginHost
from youtube_thumbnail_studio.models.canvas import Canvas
from youtube_thumbnail_studio.models.spec import Spec
from youtube_thumbnail_studio.utils.image_io import save_thumbnail

log = logging.getLogger("ytthumb.render")


class RenderService:
    def __init__(self, host: PluginHost) -> None:
        self.host = host

    def render_spec(self, spec_path: Path, out: Path) -> Path:
        spec = Spec.from_yaml(spec_path)
        canvas = Canvas(width=self.host.settings.canvas_size[0],
                        height=self.host.settings.canvas_size[1])
        canvas.metadata["title"] = spec.title

        from youtube_thumbnail_studio.services.text_service import compose_text_layers

        for layer in compose_text_layers(spec):
            canvas.push(layer)

        image = self.host.render(canvas)
        out.parent.mkdir(parents=True, exist_ok=True)
        return save_thumbnail(image, out, quality=self.host.settings.jpeg_quality)