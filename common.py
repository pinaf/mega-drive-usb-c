import bpy
import math

def cleanup():
  bpy.ops.object.select_all(action='SELECT')
  bpy.ops.object.delete(use_global=False)

def edit_mode():
  bpy.ops.object.mode_set(mode = 'EDIT')

def object_mode():
  bpy.ops.object.mode_set(mode = 'OBJECT')

def bool_diff(tool_obj, target_obj, name, delete=True):
  mod = target_obj.modifiers.new(type='BOOLEAN', name=name)
  mod.operation='DIFFERENCE'
  mod.object = tool_obj
  bpy.context.view_layer.objects.active = target_obj
  bpy.ops.object.modifier_apply(modifier=mod.name)
  if delete:
    bpy.context.view_layer.objects.active = tool_obj
    bpy.ops.object.delete()

