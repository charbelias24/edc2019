import pixy
from ctypes import *
from pixy import *
from vector_manip import *
import time
from motors import move, stop, shift_right, shift_left

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

blocks = BlockArray(100)
vectors = VectorArray(100)
intersections = IntersectionLineArray(100)
frame = 0

#Color detection frames at: Total - Threashold
FrameThreashold = 25
TotalFramePeriod = 30

BoxAhead = False
SafeToShift = True
LeftLane = True
GreenBox = 8
LeftShiftAngle = 50
BoxFoundTimeStamp = 0
TimeToSafety = 3
ShiftLaneDelay = 0.8

def detect_lines(frame):
  #print ('lines')
  if frame == 0:
    pixy.change_prog ("line")
  line_get_all_features ()
  i_count = line_get_intersections (100, intersections)
  v_count = line_get_vectors (100, vectors)

  try:
    max_vectors = filter_vectors(vectors, v_count)
    if max_vectors:
      move(degrees(get_angle(add_vectors(max_vectors))))

  except KeyboardInterrupt:
    stop()


def detect_color(frame):
  #print ('colors')
  global BoxFoundTimeStamp
  global LeftLane
  global SafeToShift
  global TimeToSafety
  global ShiftLaneDelay


  if frame == FrameThreashold:
    pixy.change_prog ("color_connected_components");
  count = pixy.ccc_get_blocks (100, blocks)

  '''  if count > 0:
    #print('frame %3d:' % (frame))
    #frame = frame + 1
    for index in range (0, count):
      print ('[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width, blocks[index].m_height))'''
  FoundBox = False
  if count > 0:
   for i in range(count):
    if(blocks[i].m_signature == GreenBox):
      FoundBox = True
      if(SafeToShift):
        BoxFoundTimeStamp = time.time()
        if(LeftLane):
          shift_right(180 - LeftShiftAngle)
          time.sleep(ShiftLaneDelay)
          LeftLane = False
          SafeToShift = False
          forward(100)
          time.sleep(0.5)
          shift_left(LeftShiftAngle)
        else:
          shift_left(LeftShiftAngle)
          time.sleep(ShiftLaneDelay)
          LeftLane = True
          SafeToShift = False
          forward(100)
          time.sleep(0.5)
          shift_right(180 - LeftShiftAngle)
        

        
  if( (not FoundBox) and ( (time.time() - BoxFoundTimeStamp) > TimeToSafety) ):
    SafeToShift = True





frame = 0


while 1:

  if frame < FrameThreashold:
    detect_lines(frame)
  else :
    detect_color(frame)
  
  frame += 1
  if frame == TotalFramePeriod:
    frame = 0
    
  #print (frame)
  
  #max_vectors = filter_vectors(vectors, v_count)


