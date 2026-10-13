"""TextService — rasterizes spec text layers with outline + shadow."""
from __future__ import annotations

from PIL import Image, ImageDraw

from youtube_thumbnail_studio.models.spec import Spec
from youtube_thumbnail_studio.utils.fonts import load_font


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def compose_text_layers(spec: Spec) -> list[Image.Image]:
    layers: list[Image.Image] = []
    for text in spec.texts:
        canvas = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        font = load_font(text.font, text.size)
        bbox = draw.textbbox((0, 0), text.text, font=font, stroke_width=text.stroke_width)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = int(text.anchor[0] * 1280 - w / 2)
        y = int(text.anchor[1] * 720 - h / 2)
        draw.text(
            (x, y),
            text.text,
            font=font,
            fill=_hex_to_rgb(text.color),
            stroke_width=text.stroke_width,
            stroke_fill=_hex_to_rgb(text.stroke),
        )
        layers.append(canvas)
    return layers