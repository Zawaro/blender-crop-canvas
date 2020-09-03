import bpy

class Crop_Canvas_Set_OT_Operator(bpy.types.Operator):
  bl_idname = "view3d.crop_canvas_set"
  bl_label = "Crop canvas operator"
  bl_description = "Crop canvas set"

  def execute(self, context):
    scene = context.scene
    crop_canvas_tool = scene.crop_canvas_tool
    resolution_x = scene.render.resolution_x
    resolution_y = scene.render.resolution_y

    dimension_x = scene.crop_canvas_tool.x_int
    dimension_y = scene.crop_canvas_tool.y_int

    if dimension_x >= resolution_x:
      dimension_x = resolution_x
    if dimension_y >= resolution_y:
      dimension_y = resolution_y

    xmin = resolution_x / 2 - dimension_x / 2
    xmax = resolution_x / 2 + dimension_x / 2
    ymin = resolution_y / 2 - dimension_y / 2
    ymax = resolution_y / 2 + dimension_y / 2

    print(xmin,xmax,ymin,ymax)

    scene.render.use_border = True
    scene.render.use_crop_to_border = True

    bpy.context.scene.render.border_min_x = xmin / resolution_x
    bpy.context.scene.render.border_max_x = xmax / resolution_x
    bpy.context.scene.render.border_min_y = ymin / resolution_y
    bpy.context.scene.render.border_max_y = ymax / resolution_y

    # bpy.ops.view3d.render_border(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
    return {'FINISHED'}

class Crop_Canvas_Reset_OT_Operator(bpy.types.Operator):
  bl_idname = "view3d.crop_canvas_reset"
  bl_label = "Crop canvas reset operator"
  bl_description = "Crop canvas reset"

  def execute(self, context):
    scene = context.scene
    crop_canvas_tool = scene.crop_canvas_tool

    scene.render.use_border = False
    scene.render.use_crop_to_border = False
    bpy.ops.view3d.clear_render_border()
    return {'FINISHED'}