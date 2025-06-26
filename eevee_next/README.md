# Blender Crop Canvas Addon: Eevee Next 1.0.0 - Blender 4.3

## Requirements

This project requires:
- **Python**: Version 3.10+ (Blender uses its own bundled or system interpreter)
- **uv**: A blazing-fast dependency installer for Python
- **Blender**: Version 4.3+ (Blender is used for this project)

## Project Setup

Install uv globally first
```bash
python -m pip install --user uv   # OR: python3 -m pip install --user uv
```

Create virtual environment with specific Python version (for Blender 4.3 addon development)
```bash
uv venv --python 3.11
source .venv/bin/activate
```

Install fake-bpy-module with the correct Blender version pinning
```bash
uv pip install fake-bpy-module-4.3==0.2.6 bpy pytest mock
```
