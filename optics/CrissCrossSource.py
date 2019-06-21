import numpy as np
from matplotlib.collections import LineCollection

import sys
sys.path.append('..')
import geometry as g

class CrissCrossSource():
  _cl = 'black'  # color on drawing
  _lw = 2        # linewidth on drawing
  def __init__(self, location1, location2, size1, size2, shape1='rectangle', shape2='circle'):
    """
    location: (x,y,z) of component
    size: (dx, dz) of component
    shape: 'rectangle' or 'circle'
    1 - upstream component; 2 - downstream component
    """
    self.loc1 = location1
    self.loc2 = location2
    self.size1 = size1
    self.size2 = size2
    self.shape1 = shape1
    self.shape2 = shape2

  def drawZX(self):
    """ Draw component on the Z-X plane (horizontal)
    """
    pass
