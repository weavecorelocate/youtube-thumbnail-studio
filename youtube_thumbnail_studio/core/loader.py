"""PluginLoader — discovers extension modules and entry-point plugins."""
from __future__ import annotations

import importlib
import importlib.metadata as md
import logging
import sys
from pathlib import Path

from youtube_thumbnail_studio.core.registry import PluginRegistry
from youtube_thumbnail_studio.models.plugin import ThumbnailPlugin

log = logging.getLogger("ytthumb.loader")

ENTRYPOINT_GROUP = "ytthumb.plugins"


class PluginLoader:
    def __init__(self, registry: PluginRegistry, paths: list[Path]) -> None:
        self.registry = registry
        self.paths = [p for p in paths if p.exists()]

    def discover(self) -> list[Path]:
        found: list[Path] = []
        for root in self.paths:
            for mod in sorted(root.rglob("*.py")):
                if mod.name.startswith("_"):
                    continue
                found.append(mod)
        log.info("discovered %d candidate plugin files", len(found))
        return found

    def _import_file(self, path: Path) -> None:
        module_name = f"ytthumb_ext_{path.parent.name}_{path.stem}"
        sys.path.insert(0, str(path.parent))
        try:
            importlib.import_module(path.stem)
        finally:
            sys.path.pop(0)

    def load_all(self) -> int:
        loaded = 0
        for ep in md.entry_points(group=ENTRYPOINT_GROUP):
            try:
                cls = ep.load()
                self.registry.register(cls())
                loaded += 1
            except Exception:  # noqa: BLE001
                log.exception("entry-point plugin %s failed to load", ep.name)
        return loaded

    def register_instance(self, plugin: ThumbnailPlugin) -> None:
        self.registry.register(plugin)