"""Batch handler — renders every .ytthumb in a folder in parallel."""
from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from youtube_thumbnail_studio.services.render_service import RenderService

log = logging.getLogger("ytthumb.batch")


def render_folder(service: RenderService, folder: Path, workers: int = 4) -> list[Path]:
    specs = sorted(folder.glob("*.ytthumb"))
    out_dir = folder / "rendered"
    out_dir.mkdir(exist_ok=True)

    def _one(spec: Path) -> Path | None:
        try:
            return service.render_spec(spec, out_dir / f"{spec.stem}.png")
        except Exception:  # noqa: BLE001
            log.exception("failed to render %s", spec.name)
            return None

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(_one, specs))
    return [r for r in results if r is not None]