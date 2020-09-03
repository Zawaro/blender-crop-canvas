# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Crop Canvas",
    "author" : "Zawaro",
    "description" : "Simple tool to crop canvas to render the only wanted area",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy


from . crop_canvas_op import Crop_Canvas_Reset_OT_Operator, Crop_Canvas_Set_OT_Operator
from . crop_canvas_panel import Crop_Canvas_PT_Panel, CropCanvasProperties

classes = (
    Crop_Canvas_Reset_OT_Operator,
    Crop_Canvas_Set_OT_Operator,
    Crop_Canvas_PT_Panel,
    CropCanvasProperties
)

def register():
    from bpy.utils import register_class
    from bpy.props import PointerProperty

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.crop_canvas_tool = PointerProperty(type=CropCanvasProperties)

def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.crop_canvas_tool

if __name__ == "__main__":
    register()
