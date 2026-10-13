"""Font resolution — bundled, user, then system fallback."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

BUNDLED = Path(__file__).resolve().parent.parent / "assets" / "fonts"
USER_DIR = Path.home() / ".ytthumb" / "fonts"


@lru_cache(maxsize=64)
def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for root in (BUNDLED, USER_DIR):
        candidate = root / f"{name}.ttf"
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default(size=size)