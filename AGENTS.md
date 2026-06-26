# AGENTS.md

## What this is

Blender addon with 4 variants for different Blender versions. Each variant is a self-contained folder with its own `__init__.py` and `crop_canvas.py`.

## Variant map

| Folder      | Blender version | Version source               |
|-------------|-----------------|------------------------------|
| `legacy/`   | 2.79b           | `bl_info` in `__init__.py`   |
| `eevee/`    | 2.80            | `bl_info` in `__init__.py`   |
| `cyclesx/`  | 3.0             | `bl_info` in `__init__.py`   |
| `eevee_next/` | 4.2          | `blender_manifest.toml`      |

## Code is duplicated, not shared

`eevee/`, `eevee_next/`, and `cyclesx/` have identical `crop_canvas.py` files. `legacy/` uses an older Blender API (no `bpy.props` class-level annotations, different handler names). When changing logic, edit all three modern variants identically. Check legacy separately.

## Version bumps

Bump in ALL of these when releasing:
- `legacy/__init__.py` — `bl_info["version"]`
- `eevee/__init__.py` — `bl_info["version"]`
- `cyclesx/__init__.py` — `bl_info["version"]`
- `eevee_next/blender_manifest.toml` — `version` field (not `schema_version`)
- `pyproject.toml` — `version`

## Release packaging

```
python zip_script.py
```

Creates `{variant}_{version}.zip` in `releases/`. Contents are wrapped under `blender_crop_canvas/` directory name. Version is parsed from `bl_info` or `blender_manifest.toml`.

## Style

- Ruff: `indent-width = 2` (non-standard, 2-space indent everywhere)
- pylint: naming convention warnings disabled (`C0103`)
- No type hints, no tests, no CI

## Gotchas

- `eevee_next/__init__.py` has no `bl_info` — it relies solely on `blender_manifest.toml` for version
- The `crop_canvas_monitor` handler runs on `depsgraph_update_post` (modern) or `scene_update_post` (legacy) — these are different Blender APIs
- Properties use `update=lambda self, ctx: self.update_canvas_region(ctx)` — the lambda pattern is intentional for Blender property callbacks
