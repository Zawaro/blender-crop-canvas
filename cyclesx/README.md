# Blender Crop Canvas Addon: CyclesX 1.0.0 - Blender 3.0

## Requirements

This project requires:
- **Python**: Version 3.9+ (Blender uses its own bundled or system interpreter)
- **uv**: A blazing-fast dependency installer for Python
- **Blender**: Version 3.0+ (Blender is used for this project)

## Project Setup

Install uv globally first
```bash
python -m pip install --user uv   # OR: python3 -m pip install --user uv
```

Create virtual environment with specific Python version (for Blender 3.0 addon development)
```bash
uv venv --python 3.9
source .venv/bin/activate
```

Install fake-bpy-module with the correct Blender version pinning
```bash
uv pip install fake-bpy-module-3.0
```
