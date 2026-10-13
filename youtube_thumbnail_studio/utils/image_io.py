"""Image I/O helpers — safe save with format inference."""
from __future__ import annotations

from pathlib import Path

from PIL import Image


def save_thumbnail(image: Image.Image, path: Path, quality: int = 92) -> Path:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        image.save(path, format="JPEG", quality=quality, optimize=True, progressive=True)
    elif suffix == ".png":
        image.save(path, format="PNG", optimize=True)
    elif suffix == ".webp":
        image.save(path, format="WEBP", quality=quality, method=6)
    else:
        raise ValueError(f"unsupported thumbnail format: {suffix}")
    return path