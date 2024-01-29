import bpy
import math

common = bpy.data.texts["common"].as_module()

# ----------------------- START -------------

# init
common.object_mode()
common.cleanup()

# base plate
base_dimensions = [26, 15.2, 1.5]
bpy.ops.mesh.primitive_cube_add()
common.edit_mode()
base_obj = bpy.context.active_object
base_obj.name = 'Base'
base_obj.scale = [dim / 2 for dim in base_dimensions]
common.object_mode()

# base hole
base_hole_diam = 5.5
bpy.ops.mesh.primitive_cylinder_add()
common.edit_mode()
base_hole = bpy.context.active_object
base_hole.name = 'Base Hole'
base_hole.location[0] = -(base_dimensions[0] / 2) + 2.2 + (base_hole_diam/2) 
base_hole.location[1] = (base_dimensions[1] / 2) - 5.3 - (base_hole_diam/2)
base_hole.scale = [base_hole_diam/2, base_hole_diam/2, 1]
common.object_mode()
common.bool_diff(base_hole, base_obj, 'Base_Hole_Mod')

# plug bed (prism)
plug_bed_dimensions = [12.2, 15, 6]
bpy.ops.mesh.primitive_cube_add()
common.edit_mode()
plug_bed_obj = bpy.context.active_object
plug_bed_obj.name = 'Plug Bed'
plug_bed_obj.scale = [dim / 2 for dim in plug_bed_dimensions]
plug_bed_obj.location[0] = -(base_dimensions[0] / 2) + 15
plug_bed_obj.location[1] = +(base_dimensions[1] / 2) - (plug_bed_dimensions[1] / 2) - 4.3
plug_bed_obj.location[2] = -(base_dimensions[2] / 2) + (plug_bed_dimensions[2] / 2)
common.object_mode()
common.bool_diff(plug_bed_obj, base_obj, 'Plug_Bed_Mod', delete=False)

# plug housing (prism)
plug_face_thickness = 2.5
plug_dimensions = [12, 8.5 - plug_face_thickness, 6]
plug_y_offset = 22.3 - 19.2 - plug_face_thickness
plug_hole_diam = 4.0
bpy.ops.mesh.primitive_cube_add()
common.edit_mode()
plug_obj = bpy.context.active_object
plug_obj.name = 'Plug Housing'
plug_obj.scale = [dim / 2 for dim in plug_dimensions]
plug_obj.location[0] = plug_bed_obj.location[0]
plug_obj.location[1] = plug_bed_obj.location[1] - plug_bed_dimensions[1] / 2 + plug_dimensions[1] / 2 - plug_y_offset
plug_obj.location[2] = plug_bed_obj.location[2] + (plug_bed_dimensions[2] / 2) + (plug_dimensions[2] / 2)
common.object_mode()
common.bool_diff(plug_obj, plug_bed_obj, 'Plug_Housing_Mod', delete=False)

# plug face (cylinder)
plug_face_dimensions = [10, 10, plug_face_thickness]
bpy.ops.mesh.primitive_cylinder_add()
common.edit_mode()
plug_face = bpy.context.active_object
plug_face.name = 'Plug Face'
plug_face.scale = [dim / 2 for dim in plug_face_dimensions]
plug_face.location[0] = plug_obj.location[0]
plug_face.location[1] = plug_obj.location[1] - plug_dimensions[1] / 2 - plug_face_dimensions[2] / 2
plug_face.location[2] = plug_bed_obj.location[2] + (plug_bed_dimensions[2] / 2) + (plug_hole_diam / 2)
plug_face.rotation_euler = [math.radians(90), 0, 0]
common.object_mode()
common.bool_diff(plug_face, plug_bed_obj, 'Plug_Face_Mod', delete=False)

# plug hole
bpy.ops.mesh.primitive_cylinder_add()
common.edit_mode()
plug_hole = bpy.context.active_object
plug_hole.name = 'Plug Hole'
plug_hole.location = plug_face.location.copy()
plug_hole.scale = [1, plug_hole_diam / 2, 15]
plug_hole.rotation_euler = [math.radians(90), 0, 0]
common.object_mode()
stretch = (9.6 - 2) / 2
for v in plug_hole.data.vertices:
  if (v.co.x < 0):
    v.co.x -= stretch
  elif (v.co.x > 0):
    v.co.x += stretch
common.bool_diff(plug_hole, plug_face, 'Plug_Hole_Mod', delete=False)
common.bool_diff(plug_hole, plug_obj, 'Plug_Hole_Mod_2')

# top shave
top_shave_dimensions = [plug_dimensions[0], 10 * plug_dimensions[2], 2.5]
top_shave_offset = 1.5
bpy.ops.mesh.primitive_cube_add()
common.edit_mode()
top_shave_obj = bpy.context.active_object
top_shave_obj.name = 'Top Shave'
top_shave_obj.scale = [dim / 2 for dim in top_shave_dimensions]
top_shave_obj.location = plug_face.location.copy()
top_shave_obj.location.y += top_shave_offset
top_shave_obj.location.z += 4
common.object_mode()
common.bool_diff(top_shave_obj, plug_obj, 'Top_Shave_Mod')

# top shave B
top_shave_b_dimensions = [plug_dimensions[0], plug_dimensions[2] + 1, 2.5]
top_shave_b_offset = -0.1
bpy.ops.mesh.primitive_cube_add()
common.edit_mode()
top_shave_b_obj = bpy.context.active_object
top_shave_b_obj.name = 'Top Shave B'
top_shave_b_obj.scale = [dim / 2 for dim in top_shave_b_dimensions]
top_shave_b_obj.location = plug_face.location.copy()
top_shave_b_obj.location.y += top_shave_b_offset
top_shave_b_obj.location.z += 5.5
common.object_mode()
common.bool_diff(top_shave_b_obj, plug_face, 'Top_Shave_B_Mod')

# bottom shave
bottom_shave_dimensions = [plug_face_dimensions[0], plug_face_dimensions[2], 0.6]
bottom_shave_offset = 2
bpy.ops.mesh.primitive_cube_add()
common.edit_mode()
bottom_shave_obj = bpy.context.active_object
bottom_shave_obj.name = 'Bottom Shave'
bottom_shave_obj.scale = [dim / 2 for dim in bottom_shave_dimensions]
bottom_shave_obj.location = plug_face.location.copy()
bottom_shave_obj.location.z -= plug_face_dimensions[1] / 2 - bottom_shave_dimensions[2] / 2
common.object_mode()
common.bool_diff(bottom_shave_obj, plug_face, 'Bottom_Shave_Mod')
