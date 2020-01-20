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
    "name" : "weld",
    "author" : "kojocrash",
    "description" : "Keeps offset without parenting",
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : 'Object'
}

import bpy
import mathutils

from .  weld_op     import *
from .  weld_panel  import WeldPanel

classes = (WELD_OT_createWeld, WELD_OT_removeWeld, WELD_OT_bakeWeld, WeldPanel)

from bpy.app.handlers import persistent


Welds = []

def updateWeld(child):
    if not "WeldData" in child:
        return

    WeldData = child["WeldData"]
    offset = mathutils.Matrix(WeldData["offset"])
    parent = pathToBone(WeldData["parentPath"])

    parCF = getWorldSpace(parent)
    targetCF = parCF @ offset
    newCF = getObjectSpace(child, targetCF)
    
    child.matrix = newCF

@persistent
def setup(dummy):
    for armature in [ob for ob in bpy.data.objects if ob.type == 'ARMATURE']:
        for bone in armature.pose.bones:
            if "WeldData" in bone:
                Welds.append(bone)
                

    if not bpy.app.timers.is_registered(updateAllWelds):
        bpy.app.timers.register(updateAllWelds)


def updateAllWelds():
    for w in Welds:
        updateWeld(w)

    return 0.5

def getWorldSpace(pose_bone):
    obj = pose_bone.id_data
    matrix_final = obj.matrix_world @ pose_bone.matrix

    return matrix_final

def getObjectSpace(pose_bone, mat):
    obj = pose_bone.id_data   
    matrix_final = mat @ obj.matrix_world.inverted()
    
    return matrix_final

def pathToBone(path):
    obj = bpy.data.objects[path[0]]
    poseBones = obj.pose.bones
    parent = None

    for x in poseBones:
        if x.name == path[1]:
            parent = x
            break
        
    return parent

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    if not setup in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(setup)

    if not bpy.app.timers.is_registered(updateAllWelds):
        bpy.app.timers.register(updateAllWelds)
    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    if setup in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(setup)
