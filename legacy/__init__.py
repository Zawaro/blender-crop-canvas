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
from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, BoolProperty, PointerProperty
from bpy.types import Panel, PropertyGroup

bl_info = {
  "name": "Crop Canvas",
  "author": "Zawaro",
  "description": "Simple tool to crop canvas to render the only wanted area",
  "blender": (2, 79, 0),
  "version": (1, 0, 0),
  "location": "View3D",
  "warning": "",
  "category": "Render",
}


def update_canvas_region(self, context):
  scene = context.scene
  render = scene.render
  crop = scene.crop_canvas_tool

  res_x = render.resolution_x
  res_y = render.resolution_y

  dim_x = min(crop.x_int, res_x)
  dim_y = min(crop.y_int, res_y)

  xmin = res_x / 2 - dim_x / 2
  xmax = res_x / 2 + dim_x / 2
  ymin = res_y / 2 - dim_y / 2
  ymax = res_y / 2 + dim_y / 2

  if crop.use_crop_canvas:
    render.use_border = True
    render.use_crop_to_border = True
    render.border_min_x = xmin / res_x
    render.border_max_x = xmax / res_x
    render.border_min_y = ymin / res_y
    render.border_max_y = ymax / res_y
  else:
    render.use_border = False
    render.use_crop_to_border = False


class CropCanvasProperties(PropertyGroup):
  use_crop_canvas = BoolProperty(
    name="Crop Canvas",
    description="Enable cropped render border",
    default=False,
    update=update_canvas_region,
  )

  x_int = IntProperty(
    name="X",
    description="X dimension of cropped render",
    default=128,
    min=0,
    max=4096,
    update=update_canvas_region,
  )

  y_int = IntProperty(
    name="Y",
    description="Y dimension of cropped render",
    default=128,
    min=0,
    max=4096,
    update=update_canvas_region,
  )


def crop_canvas_monitor_handler(scene):
  crop = scene.crop_canvas_tool
  render = scene.render

  if crop.use_crop_canvas:
    if not render.use_border or not render.use_crop_to_border:
      crop.use_crop_canvas = False  # This will trigger update


class VIEW3D_PT_crop_canvas(Panel):
  bl_idname = "VIEW3D_PT_crop_canvas"
  bl_label = "Crop Canvas"
  bl_category = "Crop Canvas"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"

  def draw(self, context):
    layout = self.layout
    crop = context.scene.crop_canvas_tool

    layout.prop(crop, "use_crop_canvas")
    layout.prop(crop, "x_int")
    layout.prop(crop, "y_int")


class RENDER_PT_crop_canvas(bpy.types.Panel):
  bl_idname = "RENDER_PT_crop_canvas"
  bl_label = "Crop Canvas"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "render"
  bl_options = {"DEFAULT_CLOSED"}

  def draw(self, context):
    layout = self.layout
    crop = context.scene.crop_canvas_tool

    layout.prop(crop, "use_crop_canvas")
    layout.prop(crop, "x_int")
    layout.prop(crop, "y_int")


classes = (
  VIEW3D_PT_crop_canvas,
  RENDER_PT_crop_canvas,
  CropCanvasProperties,
)


def register():
  for cls in classes:
    register_class(cls)

  bpy.types.Scene.crop_canvas_tool = PointerProperty(type=CropCanvasProperties)

  if crop_canvas_monitor_handler not in bpy.app.handlers.scene_update_post:
    bpy.app.handlers.scene_update_post.append(crop_canvas_monitor_handler)


def unregister():
  for cls in reversed(classes):
    unregister_class(cls)

  del bpy.types.Scene.crop_canvas_tool

  if crop_canvas_monitor_handler in bpy.app.handlers.scene_update_post:
    bpy.app.handlers.scene_update_post.remove(crop_canvas_monitor_handler)


if __name__ == "__main__":
  register()
