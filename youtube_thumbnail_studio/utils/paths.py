"""Path helpers for the ytthumb user profile."""
from __future__ import annotations

from pathlib import Path


def user_profile() -> Path:
    root = Path.home() / ".ytthumb"
    root.mkdir(parents=True, exist_ok=True)
    return root


def cache_path(*parts: str) -> Path:
    p = user_profile() / "cache"
    p.mkdir(parents=True, exist_ok=True)
    return p.joinpath(*parts)