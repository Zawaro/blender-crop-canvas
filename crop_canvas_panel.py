import bpy

from bpy.props import (IntProperty)
from bpy.types import (Panel, PropertyGroup)

class CropCanvasProperties(PropertyGroup):
  x_int: IntProperty(
    name = "X",
    description = "X dimension of cropped render",
    default = 128,
    min = 0,
    max = 4096
  )

  y_int: IntProperty(
    name = "Y",
    description = "Y dimension of cropped render",
    default = 128,
    min = 0,
    max = 4096
  )

class Crop_Canvas_PT_Panel(bpy.types.Panel):
  bl_idname = "Crop_Canvas_PT_Panel"
  bl_label = "Crop Canvas"
  bl_category = "Crop Canvas"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"

  def draw(self, context):
    layout = self.layout
    scene = context.scene
    crop_canvas_tool = scene.crop_canvas_tool

    labelrow = layout.row()
    labelrow.label(text="Resolution")

    layout.prop(crop_canvas_tool, "x_int")
    layout.prop(crop_canvas_tool, "y_int")

    set_op = layout.row()
    set_op.operator('view3d.crop_canvas_set', text="Crop Canvas")

    reset_op = layout.row()
    reset_op.operator('view3d.crop_canvas_reset', text="Reset")