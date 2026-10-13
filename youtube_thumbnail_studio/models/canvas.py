"""Canvas — the mutable render target passed through every stage."""
from __future__ import annotations

from dataclasses import dataclass, field

from PIL import Image


@dataclass
class Canvas:
    width: int = 1280
    height: int = 720
    layers: list[Image.Image] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    def push(self, layer: Image.Image) -> None:
        if layer.size != (self.width, self.height):
            layer = layer.resize((self.width, self.height), Image.LANCZOS)
        self.layers.append(layer.convert("RGBA"))

    def flatten(self) -> Image.Image:
        base = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 255))
        for layer in self.layers:
            base = Image.alpha_composite(base, layer)
        return base.convert("RGB")