import bpy

class WeldPanel(bpy.types.Panel):
    bl_idname = "WELD_PT_Panel"
    bl_label = "Weld"
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator('object.weld_create', text="Create Weld")

        row2 = layout.row()
        row2.operator('object.weld_remove', text="Remove Weld")

        layout.split()

        row3 = layout.row()
        row3.operator('object.weld_bake', text="Bake Weld to Animation")
        