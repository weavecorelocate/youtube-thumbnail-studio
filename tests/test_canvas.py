from __future__ import annotations

from PIL import Image

from youtube_thumbnail_studio.models.canvas import Canvas


def test_push_resizes_to_canvas() -> None:
    c = Canvas(width=1280, height=720)
    c.push(Image.new("RGB", (320, 180), (255, 0, 0)))
    assert c.layers[0].size == (1280, 720)


def test_flatten_returns_rgb() -> None:
    c = Canvas()
    c.push(Image.new("RGBA", (1280, 720), (0, 255, 0, 128)))
    out = c.flatten()
    assert out.mode == "RGB"
    assert out.size == (1280, 720)