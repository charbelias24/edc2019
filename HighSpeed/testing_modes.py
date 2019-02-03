import pixy
from ctypes import *
from pixy import *
from vector_manip import *
import time

# pixy2 Python SWIG get line features example #

print ("Pixy2 Python SWIG Example -- Get Line Features")

pixy.init ()

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

class Blocks (Structure):
  _fields_ = [ ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    ("m_width", c_uint),
    ("m_height", c_uint),
    ("m_angle", c_uint),
    ("m_index", c_uint),
    ("m_age", c_uint) ]

blocks = BlockArray(5)
vectors = VectorArray(5)
frame = 0

def detect_lines(frame):
  #print ('lines')
  if frame == 0:
    pixy.change_prog ("line")
  line_get_all_features ()
  v_count = line_get_vectors (5, vectors)
'''
  if v_count > 0:
    #print ('frame %3d:' % (frame))
    #frame = frame + 1
    for index in range (0, v_count):
      print ('[VECTOR: (%3d %3d) (%3d %3d)]' % (vectors[index].m_x0, vectors[index].m_y0, vectors[index].m_x1, vectors[index].m_y1))
'''     
def detect_color(frame):
  #print ('colors')

  if frame == 20:
    pixy.change_prog ("color_connected_components");
  count = pixy.ccc_get_blocks (5, blocks)

'''  if count > 0:
    #print('frame %3d:' % (frame))
    #frame = frame + 1
    for index in range (0, count):
      print ('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width, blocks[index].m_height))
'''
frame = 0

duration = time.time()

while 1:

  if frame < 20:
    detect_lines(frame)
  else :
    detect_color(frame)
  
  frame += 1
  if frame == 30:
    frame = 0
    duration = time.time() - duration
    print (duration)
    print (30 / duration)
    duration = time.time()
    
  #print (frame)
  
  #max_vectors = filter_vectors(vectors, v_count)


