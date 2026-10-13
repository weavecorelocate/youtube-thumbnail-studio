# Contributing to youtube-thumbnail-studio

Thanks for wanting to help build the studio. This is a plugin-host tool —
most contributions land as extensions, not host changes.

## Dev setup

```bash
git clone https://github.com/yourname/youtube-thumbnail-studio
cd youtube-thumbnail-studio
python -m venv .venv && .venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
```

## What to contribute

- **Extensions** — drop a folder under `plugins/`, add `plugin.py` with a
  `ThumbnailPlugin`-shaped class and a `ytthumb_plugin.toml` manifest.
  The loader discovers it on next start.
- **Host changes** — keep the four-stage pipeline (load / compose / post /
  encode) intact. Stages are a contract; extensions depend on them.
- **Bug reports** — include `ytthumb --version`, OS build, and the failing
  `.ytthumb` spec.

## Style

- `ruff` for lint, `mypy --strict` for types. CI blocks on both.
- Plugin failures must not kill the host: catch, log, continue.
- No global state in extensions. Everything you need lives on `ctx`.

## PR checklist

- [ ] `pytest -q` passes
- [ ] `ruff check .` clean
- [ ] New plugin has a `meta` with a unique `name`
- [ ] Docs updated if you touched the CLI surface

## Code of conduct

Be normal. Ship things. Don't be a dick in issues.