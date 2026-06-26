import bpy


class CropCanvasProperties(bpy.types.PropertyGroup):
  use_crop_canvas: bpy.props.BoolProperty(
    name="Crop Canvas",
    description="Enable cropped render border",
    default=False,
    update=lambda self, ctx: self.update_canvas_region(ctx),
  )

  x_int: bpy.props.IntProperty(
    name="Canvas X",
    description="X dimension of cropped render",
    default=128,
    min=0,
    max=4096,
    subtype="PIXEL",
    update=lambda self, ctx: self.update_canvas_region(ctx),
  )

  y_int: bpy.props.IntProperty(
    name="Y",
    description="Y dimension of cropped render",
    default=128,
    min=0,
    max=4096,
    subtype="PIXEL",
    update=lambda self, ctx: self.update_canvas_region(ctx),
  )

  offset_x: bpy.props.IntProperty(
    name="Offset X",
    description="Horizontal shift from center",
    default=0,
    min=-4096,
    max=4096,
    subtype="PIXEL",
    update=lambda self, ctx: self.update_canvas_region(ctx),
  )

  offset_y: bpy.props.IntProperty(
    name="Y",
    description="Vertical shift from center",
    default=0,
    min=-4096,
    max=4096,
    subtype="PIXEL",
    update=lambda self, ctx: self.update_canvas_region(ctx),
  )

  def update_canvas_region(self, context):
    render = context.scene.render
    res_x = render.resolution_x
    res_y = render.resolution_y

    dim_x = min(self.x_int, res_x)
    dim_y = min(self.y_int, res_y)

    max_offset_x = res_x / 2 - dim_x / 2
    max_offset_y = res_y / 2 - dim_y / 2

    offset_x = max(-max_offset_x, min(self.offset_x, max_offset_x))
    offset_y = max(-max_offset_y, min(self.offset_y, max_offset_y))

    xmin = res_x / 2 - dim_x / 2 + offset_x
    xmax = res_x / 2 + dim_x / 2 + offset_x
    ymin = res_y / 2 - dim_y / 2 + offset_y
    ymax = res_y / 2 + dim_y / 2 + offset_y

    if self.use_crop_canvas:
      render.use_border = True
      render.use_crop_to_border = True
      render.border_min_x = xmin / res_x
      render.border_max_x = xmax / res_x
      render.border_min_y = ymin / res_y
      render.border_max_y = ymax / res_y
    else:
      render.use_border = False
      render.use_crop_to_border = False
      render.border_min_x = 0.0
      render.border_max_x = 1.0
      render.border_min_y = 0.0
      render.border_max_y = 1.0


class VIEW3D_PT_crop_canvas_panel(bpy.types.Panel):
  bl_idname = "VIEW3D_PT_crop_canvas_panel"
  bl_label = "Crop Canvas"
  bl_category = "Crop Canvas"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"

  def draw(self, context):
    draw_crop_canvas(self, context)


def draw_crop_canvas(self, context):
  layout = self.layout
  crop = context.scene.crop_canvas_tool

  layout.use_property_split = True
  layout.use_property_decorate = False  # No animation.
  layout.prop(crop, "use_crop_canvas")
  layout.prop(crop, "x_int")
  layout.prop(crop, "y_int")
  layout.prop(crop, "offset_x")
  layout.prop(crop, "offset_y")


def crop_canvas_monitor(scene):
  crop = scene.crop_canvas_tool
  render = scene.render

  if crop.use_crop_canvas:
    if not render.use_border or not render.use_crop_to_border:
      crop.use_crop_canvas = False  # This will trigger update_canvas_region()
