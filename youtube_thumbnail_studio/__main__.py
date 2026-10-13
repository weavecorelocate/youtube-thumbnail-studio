"""Bootstrap entry point. Wires host, loader, registry, and CLI together."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import typer
from rich.console import Console

from youtube_thumbnail_studio.config.settings import StudioSettings
from youtube_thumbnail_studio.core.host import PluginHost
from youtube_thumbnail_studio.core.loader import PluginLoader
from youtube_thumbnail_studio.core.registry import PluginRegistry
from youtube_thumbnail_studio.services.render_service import RenderService

app = typer.Typer(add_completion=False, help="youtube-thumbnail-studio CLI")
console = Console()


def _bootstrap(settings: StudioSettings) -> PluginHost:
    registry = PluginRegistry()
    loader = PluginLoader(registry, settings.plugin_paths)
    loader.discover()
    loader.load_all()
    return PluginHost(registry=registry, settings=settings)


@app.command()
def render(
    spec: Path = typer.Argument(..., exists=True, readable=True, help="Path to a .ytthumb spec"),
    out: Path = typer.Option(Path("out/thumb.png"), "--out", "-o"),
) -> None:
    """Render a single .ytthumb spec through the plugin pipeline."""
    settings = StudioSettings.load()
    host = _bootstrap(settings)
    service = RenderService(host)
    written = service.render_spec(spec, out)
    console.print(f"[green]rendered[/green] {written} ({written.stat().st_size} bytes)")


@app.command("list-plugins")
def list_plugins() -> None:
    """List loaded extensions and their declared contracts."""
    settings = StudioSettings.load()
    host = _bootstrap(settings)
    for name, meta in host.registry.describe().items():
        console.print(f"{name}\t{meta.version}\t{meta.kind}\t{meta.summary}")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(name)s %(levelname)s %(message)s")
    try:
        app()
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()