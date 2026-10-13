"""Declarative .ytthumb spec — YAML on disk, validated into this model."""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class TextLayerSpec(BaseModel):
    text: str
    font: str = "Inter-Black"
    size: int = 96
    color: str = "#FFFFFF"
    stroke: str = "#000000"
    stroke_width: int = 6
    anchor: tuple[float, float] = (0.5, 0.5)


class Spec(BaseModel):
    title: str
    background: Path | None = None
    texts: list[TextLayerSpec] = Field(default_factory=list)
    effects: list[str] = Field(default_factory=list)
    output: Path = Path("out/thumb.png")

    @classmethod
    def from_yaml(cls, path: Path) -> "Spec":
        with path.open("r", encoding="utf-8") as fh:
            return cls(**yaml.safe_load(fh))