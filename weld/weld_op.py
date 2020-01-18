import bpy

class WELD_OT_createWeld(bpy.types.Operator):
    bl_idname = "view3d.weld_create"
    bl_label = "Create Weld"
    bl_description = "Creates a Weld"

    def execute(self, context):
        print("Hello World")
        return {'FINISHED'}