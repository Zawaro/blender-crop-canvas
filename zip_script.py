import os
import zipfile
import re
import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
TARGET_DIR = PROJECT_ROOT / "releases"
FOLDERS_TO_ZIP = ["legacy", "eevee", "eevee_next", "cyclesx"]
IGNORE_DIRS = {".venv"}
IGNORE_FILES = {"README.md", "requirements.txt"}
ZIP_ROOT_DIR_NAME = "blender_crop_canvas"


def parse_version_from_init(folder: Path):
  init_file = folder / "__init__.py"
  if init_file.exists():
    with open(init_file, "r", encoding="utf-8") as f:
      content = f.read()
      match = re.search(r"bl_info\s*=\s*(\{.*?\})", content, re.DOTALL)
      if match:
        bl_info = ast.literal_eval(match.group(1))
        version = bl_info.get("version")
        if isinstance(version, (list, tuple)):
          return "-".join(map(str, version))
  return None


def parse_version_from_toml(folder: Path):
  toml_file = folder / "blender_manifest.toml"
  if toml_file.exists():
    with open(toml_file, "r", encoding="utf-8") as f:
      for line in f:
        if line.strip().startswith("version"):
          match = re.search(r'version\s*=\s*"([^"]+)"', line)
          if match:
            return match.group(1).replace(".", "-")
  return None


def get_version(folder: Path):
  return parse_version_from_init(folder) or parse_version_from_toml(folder) or "0-0-0"


def zip_folder_contents(folder: Path):
  version = get_version(folder)
  zip_name = f"{folder.name}_{version}.zip"
  zip_path = TARGET_DIR / zip_name

  with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(folder):
      # Skip ignored dirs
      dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
      for file in files:
        if file in IGNORE_FILES:
          continue
        full_path = Path(root) / file
        relative_path = full_path.relative_to(folder)
        arcname = Path(ZIP_ROOT_DIR_NAME) / relative_path
        zipf.write(full_path, arcname)

  print(f"Zipped {folder.name} -> {zip_path}")


def main():
  TARGET_DIR.mkdir(exist_ok=True)
  for folder_name in FOLDERS_TO_ZIP:
    folder_path = PROJECT_ROOT / folder_name
    if folder_path.is_dir():
      zip_folder_contents(folder_path)
    else:
      print(f"Warning: {folder_name}/ not found, skipping.")


if __name__ == "__main__":
  main()
