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

from .  weld_op     import *
from .  weld_panel  import WeldPanel

classes = (WELD_OT_createWeld, WELD_OT_removeWeld, WELD_OT_bakeWeld, WeldPanel)

register, unregister = bpy.utils.register_classes_factory(classes)
