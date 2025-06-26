# Crop Canvas – a Blender addon
# Copyright (C) 2025 Zawaro (zawaroarts@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy
from bpy.utils import register_class
from bpy.props import PointerProperty
from bpy.utils import unregister_class

from .crop_canvas import (
  VIEW3D_PT_crop_canvas_panel,
  CropCanvasProperties,
  crop_canvas_monitor,
  draw_crop_canvas,
)

classes = (
  VIEW3D_PT_crop_canvas_panel,
  CropCanvasProperties,
)


def crop_canvas_monitor_handler(scene):
  crop_canvas_monitor(scene)


def register():
  for cls in classes:
    register_class(cls)

  bpy.types.Scene.crop_canvas_tool = PointerProperty(type=CropCanvasProperties)
  bpy.types.RENDER_PT_format.append(draw_crop_canvas)

  if crop_canvas_monitor_handler not in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.append(crop_canvas_monitor_handler)


def unregister():
  for cls in reversed(classes):
    unregister_class(cls)

  del bpy.types.Scene.crop_canvas_tool
  bpy.types.RENDER_PT_format.remove(draw_crop_canvas)

  if crop_canvas_monitor_handler in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.remove(crop_canvas_monitor_handler)


if __name__ == "__main__":
  register()
