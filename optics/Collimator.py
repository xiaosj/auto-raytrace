import numpy as np
from matplotlib.collections import LineCollection

import sys
sys.path.append('..')
import geometry as g

class Collimator():
  """ Class of donut-shape collimator pependicular to nominal direction
  """
  _nA = 20       # number of angular bins
  _cl = 'red'    # color on drawing
  _lw = 2        # linewidth on drawing
  def __init__(self, name, location, innerD, outterD):
    """
    name: string of name
    location: (x,y,z) front surface of collimator
    innerD, outterD: inner and outter diameter of collimator
    """
    self.name = name
    self.loc = np.array(location, dtype=np.float32)
    self.iR  = innerD * 0.5
    self.oR  = outterD * 0.5
    self.norm = np.array([0., 0., 1.], dtype=np.float32)

  def setXYfromMirror(self, mirror):
    """ Calculate X & Y coordinates from the reflection of a mirror
    """
    self.loc[0] = mirror.loc[0] + mirror.out[0] / mirror.out[2] * (self.loc[2] - mirror.loc[2])
    self.loc[1] = mirror.loc[1] + mirror.out[1] / mirror.out[2] * (self.loc[2] - mirror.loc[2])
    self.norm = mirror.out

  def drawZX(self):
    """ Draw component on the Z-X plane (horizontal)
    """
    rot = g.rot2D(self.norm[0])
    p0 = np.array([self.loc[2], self.loc[0]])
    v1 = rot.dot([0., self.iR])
    v2 = rot.dot([0., self.oR])
    segs = np.array([ [p0+v1, p0+v2],
                      [p0-v1, p0-v2]], dtype=np.float32)
    ls = LineCollection(segs, linewidths=self._lw, colors=self._cl)

    # update draw region
    self.draw_min = np.array([segs[:,:,1].min(), segs[:,:,0].min()])
    self.draw_max = np.array([segs[:,:,1].max(), segs[:,:,0].max()])

    return ls
