import numpy as np
from matplotlib.collections import LineCollection

import sys
sys.path.append('..')
import geometry as g

class CrissCrossSource():
  _cl = 'black'  # color on drawing
  _lw = 2        # linewidth on drawing
  def __init__(self, location1, location2, size1, size2):
    """
    location: (x,y,z) of component
    size: (dx, dz) of component
    1 - upstream component; 2 - downstream component
    """
    self.loc1 = location1
    self.loc2 = location2
    self.size1 = size1
    self.size2 = size2

  def getOneRay(self):
    # upstream point
    theta1 = 2 * np.pi * np.random.rand()
    radius1 = np.sqrt(np.random.rand()) * self.size1 / 2
    x1 = radius1 * np.cos(theta1) + self.loc1[2]
    y1 = radius1 * np.sin(theta1) + self.loc1[0]

    # downstream point
    theta2 =  2 * np.pi * np.random.rand()
    radius2 = np.sqrt(np.random.rand()) * self.size2 / 2
    x2 = radius2 * np.cos(theta2) + self.loc2[2]
    y2 = radius2 * np.sin(theta2) + self.loc2[0]
    return np.array([[x1, y1], [x2, y2]])

  def drawZX(self):
    """ Draw component on the Z-X plane (horizontal)
    """
    p1 = [self.loc1[2], self.loc1[0] + self.size1 / 2]
    p2 = [self.loc1[2], self.loc1[0] - self.size1 / 2]
    segs = np.array([[p1,p2]])
    ls = LineCollection(segs, linewidths = 2, colors = 'black')
    
    self.draw_min = np.array([segs[:,:,1].min(), segs[:,:,0].min()])
    self.draw_max = np.array([segs[:,:,1].max(), segs[:,:,0].max()])
    return ls

