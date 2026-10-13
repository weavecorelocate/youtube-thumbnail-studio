"""Shared contracts every thumbnail extension implements."""
from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable

from pydantic import BaseModel

from youtube_thumbnail_studio.models.canvas import Canvas


class Stage(str, Enum):
    LOAD = "load"
    COMPOSE = "compose"
    POST = "post"
    ENCODE = "encode"


class PluginKind(str, Enum):
    SOURCE = "source"
    EFFECT = "effect"
    ANALYZER = "analyzer"
    EXPORTER = "exporter"


class PluginMeta(BaseModel):
    name: str
    version: str
    kind: PluginKind
    stage: Stage
    priority: int = 100
    summary: str = ""


@runtime_checkable
class ThumbnailPlugin(Protocol):
    meta: PluginMeta

    def apply(self, ctx: "HostContextLike") -> Canvas: ...


class HostContextLike(Protocol):
    settings: object
    stage: Stage
    canvas: Canvas