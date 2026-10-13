"""CLI handlers kept separate from __main__ so they stay testable."""
from __future__ import annotations

from pathlib import Path

from rich.console import Console

from youtube_thumbnail_studio.services.ctr_service import salience_score
from youtube_thumbnail_studio.services.render_service import RenderService

console = Console()


def handle_render(service: RenderService, spec: Path, out: Path) -> int:
    written = service.render_spec(spec, out)
    console.print(f"[green]ok[/green] {written}")
    return 0


def handle_score(image: Path) -> int:
    from PIL import Image

    with Image.open(image) as img:
        score = salience_score(img.convert("RGB"))
    console.print(f"salience={score}")
    return 0