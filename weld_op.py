import bpy
import mathutils
import json

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def getWorldSpace(pose_bone):
    obj = pose_bone.id_data
    matrix_final = obj.matrix_world @ pose_bone.matrix

    return matrix_final

def boneToPath(bone):
    armatureObj = bone.id_data
    #armature = armatureObj.data
    
    bonePath = []
    bonePath.append(armatureObj.name)
    bonePath.append(bone.name)

    return bonePath

def updateWeld(child):
    if not "WeldData" in child:
        return

    WeldData = child["WeldData"]
    offset = dictToMatrix(WeldData["offset"])
    parent = pathToBone(WeldData["parentPath"])

class WELD_OT_createWeld(bpy.types.Operator):
    bl_idname = "object.weld_create"
    bl_label = "Create Weld"
    bl_description = "Welds 1st selection to 2nd"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ctx = bpy.context
        bones = ctx.selected_pose_bones

        if bones is not None and len(bones) >= 2:
            child = bones[0]
            parent = bones[1]

            CF1 = getWorldSpace(child)
            CF2 = getWorldSpace(parent)

            offset = CF2.inverted() @ CF1
            
            parentPath = boneToPath(parent)
            data = {
                "parentPath" : parentPath,
                "offset" : offset
            }

            child["WeldData"] = data

            #updateWeld(child)
        else:
            ShowMessageBox("Please select 2 bones", "Weld Error", 'ERROR')
            
        return {'FINISHED'}


class WELD_OT_removeWeld(bpy.types.Operator):
    bl_idname = "object.weld_remove"
    bl_label = "Remove Weld"
    bl_description = "Removes Weld from the Selected Bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ctx = bpy.context
        bones = ctx.selected_pose_bones

        if bones is not None and len(bones) >= 1:
            child = bones[0]
            if "WeldData" in child:
                del child["WeldData"]
        else:
            ShowMessageBox("Please select a bone with a weld", "Weld Error", 'ERROR')

        return {'FINISHED'}


class WELD_OT_bakeWeld(bpy.types.Operator):
    bl_idname = "object.weld_bake"
    bl_label = "Bake weld to animator"
    bl_description = "Applies weld in your animation"

    def execute(self, context):
        print("Baking weld")
        return {'FINISHED'}

