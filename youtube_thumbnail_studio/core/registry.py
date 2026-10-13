"""PluginRegistry — ordered, typed store of loaded extensions."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from youtube_thumbnail_studio.models.plugin import PluginMeta, Stage, ThumbnailPlugin


@dataclass(slots=True)
class _Entry:
    plugin: ThumbnailPlugin
    meta: PluginMeta


class PluginRegistry:
    def __init__(self) -> None:
        self._by_stage: dict[Stage, list[_Entry]] = defaultdict(list)
        self._by_name: dict[str, _Entry] = {}

    def register(self, plugin: ThumbnailPlugin) -> None:
        meta = plugin.meta
        if meta.name in self._by_name:
            raise ValueError(f"duplicate plugin name: {meta.name}")
        entry = _Entry(plugin=plugin, meta=meta)
        self._by_name[meta.name] = entry
        self._by_stage[meta.stage].append(entry)
        self._by_stage[meta.stage].sort(key=lambda e: e.meta.priority)

    def for_stage(self, stage: Stage) -> list[ThumbnailPlugin]:
        return [e.plugin for e in self._by_stage.get(stage, [])]

    def describe(self) -> dict[str, PluginMeta]:
        return {name: e.meta for name, e in self._by_name.items()}