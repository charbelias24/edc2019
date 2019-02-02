import pixy
from ctypes import *
from pixy import *
from vector_manip import *
from motors import move, stop

# pixy2 Python SWIG get line features example #

print ("Pixy2 Python SWIG Example -- Get Line Features")

pixy.init ()
pixy.change_prog ("line")

class Vector (Structure):
  _fields_ = [
    ("m_x0", c_uint),
    ("m_y0", c_uint),
    ("m_x1", c_uint),
    ("m_y1", c_uint),
    ("m_index", c_uint),
    ("m_flags", c_uint) ]

class IntersectionLine (Structure):
  _fields_ = [
    ("m_index", c_uint),
    ("m_reserved", c_uint),
    ("m_angle", c_uint) ]

vectors = VectorArray(100)
intersections = IntersectionLineArray(100)
frame = 0

while 1:
  line_get_all_features ()
  i_count = line_get_intersections (100, intersections)
  v_count = line_get_vectors (100, vectors)
  '''
  if i_count > 0 or v_count > 0:
    print ('frame %3d:' % (frame))
    frame = frame + 1
    for index in range (0, i_count):
      print ('[INTERSECTION: INDEX=%d ANGLE=%d]' % (intersections[index].m_index, intersections[index].m_angle))
    for index in range (0, v_count):
      print ('[VECTOR: (%3d %3d) (%3d %3d)]' % (vectors[index].m_x0, vectors[index].m_y0, vectors[index].m_x1, vectors[index].m_y1))
  '''    
  try:
    max_vectors = filter_vectors(vectors, v_count)
    if max_vectors:
      move(degrees(get_angle(add_vectors(max_vectors))))

  except KeyboardInterrupt:
    stop()

    #print(max_vectors)
    
