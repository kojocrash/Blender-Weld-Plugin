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

def vectorToDict(vec):
    tempDict = {
        "px" : vec.x,
        "py" : vec.y,
        "pz" : vec.z
    }

    return tempDict

def quatToDict(quat):
    tempDict = {
        "qw" : quat.w,
        "qx" : quat.x,
        "qy" : quat.y,
        "qz" : quat.z
    }

    return tempDict

def dictToVector(dic):
    return mathutils.Vector((dic["px"], dic["py"], dic["pz"]))

def dictToQuat(dic):
    return mathutils.Quaternion((dic["qw"], dic["qx"], dic["qy"], dic["qz"]))

def matrixToDict(mat):
    vec = vectorToDict(mat.to_translation())
    quat = quatToDict(mat.to_quaternion())

    offsetData = dict(vec, **quat)
    return offsetData

def dictToMatrix(dic):
    translation = dictToVector(dic)
    quat = dictToQuat(dic)

    mat_quat = quat.to_matrix()
    mat_quat.resize_4x4()
    mat_trans = mathutils.Matrix.Translation(translation) - mathutils.Matrix()
    
    mat = mat_quat + mat_trans
    return mat

class WELD_OT_createWeld(bpy.types.Operator):
    bl_idname = "object.weld_create"
    bl_label = "Create Weld"
    bl_description = "Welds 1st selection to 2nd"

    def execute(self, context):
        ctx = bpy.context
        bones = ctx.selected_pose_bones

        if bones is not None and len(bones) >= 2:
            child = bones[0]
            parent = bones[1]

            CF1 = getWorldSpace(child)
            CF2 = getWorldSpace(parent)

            offset = CF1 @ CF2.inverted()
            offsetData = matrixToDict(offset)
            
            armatureObj = parent.id_data

            #testDecompose = dictToMatrix(offsetData)
        else:
            ShowMessageBox("Please select 2 bones", "Weld Error", 'ERROR')

        return {'FINISHED'}


class WELD_OT_removeWeld(bpy.types.Operator):
    bl_idname = "object.weld_remove"
    bl_label = "Remove Weld"
    bl_description = "Removes Weld from the Selected Bone"

    def execute(self, context):
        print("Removing weld")
        return {'FINISHED'}


class WELD_OT_bakeWeld(bpy.types.Operator):
    bl_idname = "object.weld_bake"
    bl_label = "Bake weld to animator"
    bl_description = "Applies weld in your animation"

    def execute(self, context):
        print("Baking weld")
        return {'FINISHED'}