import bpy

class WeldPanel(bpy.types.Panel):
    bl_idname = "Weld_PT_Panel"
    bl_label = "Weld Panel"
    bl_category = "Weld Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator('view3d.weld_create', text="Create Weld")
        
        