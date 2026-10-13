from __future__ import annotations

import pytest

from youtube_thumbnail_studio.core.registry import PluginRegistry
from youtube_thumbnail_studio.models.canvas import Canvas
from youtube_thumbnail_studio.models.plugin import PluginKind, PluginMeta, Stage


class _Noop:
    meta = PluginMeta(
        name="test.noop",
        version="0.0.1",
        kind=PluginKind.EFFECT,
        stage=Stage.POST,
        priority=50,
    )

    def apply(self, ctx):
        return ctx.canvas


def test_register_and_describe() -> None:
    reg = PluginRegistry()
    reg.register(_Noop())
    assert "test.noop" in reg.describe()
    assert reg.for_stage(Stage.POST)[0].meta.name == "test.noop"


def test_duplicate_name_rejected() -> None:
    reg = PluginRegistry()
    reg.register(_Noop())
    with pytest.raises(ValueError):
        reg.register(_Noop())


def test_priority_ordering() -> None:
    class _Low(_Noop):
        meta = PluginMeta(
            name="test.low", version="0.0.1", kind=PluginKind.EFFECT,
            stage=Stage.POST, priority=900,
        )

    reg = PluginRegistry()
    reg.register(_Low())
    reg.register(_Noop())
    assert [p.meta.name for p in reg.for_stage(Stage.POST)] == ["test.noop", "test.low"]