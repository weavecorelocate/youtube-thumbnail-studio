"""Runtime settings loaded from ytthumb.toml / env vars."""
from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field

DEFAULT_PLUGIN_DIRS = (
    Path.home() / ".ytthumb" / "plugins",
    Path("plugins"),
)


class StudioSettings(BaseModel):
    plugin_paths: list[Path] = Field(default_factory=lambda: list(DEFAULT_PLUGIN_DIRS))
    cache_dir: Path = Path.home() / ".ytthumb" / "cache"
    canvas_size: tuple[int, int] = (1280, 720)
    jpeg_quality: int = 92
    max_workers: int = max(2, (os.cpu_count() or 4) - 1)

    @classmethod
    def load(cls, path: Path | None = None) -> "StudioSettings":
        path = path or Path("ytthumb.toml")
        if path.exists():
            import tomllib

            with path.open("rb") as fh:
                raw = tomllib.load(fh)
            return cls(**raw.get("studio", {}))
        return cls()