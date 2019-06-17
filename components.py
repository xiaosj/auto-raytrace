import numpy as np
import geometry as g
from matplotlib.collections import LineCollection


def ComponentList(comps, endZ=None):
  """ Sort component list based on their Z-coordinate and define the end Z
        If endZ=None, endZ = Z of the last component + 1 meter
  """
  comp_list = comps.sort(key=lambda comp: comp.loc[2])
  # if endZ = None:

  return comp_list


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


class FlatMirror():
  """
  Class of a flat mirror
  Properties:
  * name: str, mirror name
  * loc: (3,) nominal X/Y/Z; half_size: (3,) half of X/Y/Z dimensions
  * A: nominal angle in rad; dA: (2,) rotation angle (-,+); ndA: # of angle divisions
  * trans: (2,) translation range (-,+); ntrans: # of translation division
  * horizontal: bool, horizontal or vertical if not
  * sign: +/-1 to indicate the mirror orientation
  * norm: norm vector at nominal; inp: incident norm vector; out: output norm vector
  * refl: (ndA * ntrans, 6) reflection surfaces, each plain is defined as point (3,) and norm (3,)
  * front: (ndA * ntrans, 6) front surfaces, each plain is defined as point (3,) and norm (3,)
  """
  _cl = 'red'  # color on drawing
  _lw = 1      # linewidth on drawing
  def __init__(self, name, location, size, direction, A, deltaA, translation, incidentNorm, ndA=11, ntrans=5):
    """
    Parmaeters:
        name: string of name
        location: (x,y,z) center of reflection surface at nominal location
        size: (x,y,z) size of mirror
        direction: 'x' or 'X' for horinzontal refelction; 'y' or 'Y' for vertical reflection
        incidentA: incident angle in rad
        deltaA: (-dA, +dA) mirror rotation range in rad
        translation: (-d, +d) mirror translation range: '+' into beams, '-' out of beams
        incidentNorm: (3,) normoalized incident beam on the primary direction
        ndA: number of divisions on rotation (inclusive on both ends)
        ntrans: number of divisions on translation (inclusive on both ends)
    """
    self.name = name
    self.loc = np.array(location, dtype=np.float32)
    self.half_size = np.array(size, dtype=np.float32) * 0.5
    self.sign = 1 if(A > 0) else -1
    if(direction == 'x' or direction == 'X'):
      self.horizontal = True
      self.norm = np.array([np.cos(A)*self.sign, 0., -np.abs(np.sin(A))], dtype=np.float32)
    elif(direction == 'y' or direction == 'Y'):
      self.horizontal = False
      self.norm = np.array([0., np.cos(A)*self.sign, -np.abs(np.sin(A))], dtype=np.float32)
    else:
      raise ('Wrong direction {:}.  Must be X or Y'.format(direction))
    self.A = A
    self.dA = np.array(deltaA, dtype=np.float32)
    self.trans = np.array(translation, dtype=np.float32)
    self.inp = g.VectorNormalize(incidentNorm)        # primary input  beam (normalized)
    self.out = g.Reflection(incidentNorm, self.norm)  # primary output beam (normalized)
    self.ndA = ndA
    self.ntrans = ntrans
    self._initSurfaces()

  def _initSurfaces(self):
    # initialize mirror reflection and front surfaces on each dvision
    self.refl = np.zeros((self.ndA*self.ntrans, 6), dtype=np.float32)
    self.front = np.zeros_like(self.refl)
    for iA in range(self.ndA):
      A = self.A + self.dA[0] + (self.dA[1] - self.dA[0]) * iA / (self.ndA - 1)
      for iX in range(self.ntrans):
        trans = self.trans[0] + (self.trans[1] - self.trans[0]) * iX / (self.ntrans - 1)

  def setXYfromMirror(self, mirror):
    pass
    
  def drawZX(self):
    """ Draw component on the Z-X plane (horizontal)
    """
    if(self.horizontal):  # horizontal reflection
      # mirror body
      rot =g.rot2D(self.A)
      p0 = np.array([self.loc[2], self.loc[0]])
      v1 = rot.dot([self.half_size[2], 0.])
      v2 = rot.dot([0., -self.sign * self.half_size[0]])
      mirror_segs = np.array([p0+v1, p0-v1, p0-v1+v2, p0+v1+v2, p0+v1], dtype=np.float32)
      self.draw_min = np.array([mirror_segs[:,1].min(),
                                mirror_segs[:,0].min()],
                              dtype=np.float32)
      self.draw_max = np.array([mirror_segs[:,1].max(),
                                mirror_segs[:,0].max()],
                              dtype=np.float32)

      # mirror motion range
      dz  = self.half_size[2] * np.cos(self.A - self.dA)
      dx1 = self.half_size[2] * np.sin(np.abs(self.A) + self.dA)
      dx2 = self.half_size[2] * np.sin(np.abs(self.A) - self.dA)
      range_segs = np.array([
                      (self.loc[2] + dz,
                       self.loc[0] + (self.trans[0] + dx1) * self.sign),
                      (self.loc[2] - dz,
                       self.loc[0] + (self.trans[0] - dx2) * self.sign),
                      (self.loc[2] - dz,
                       self.loc[0] - (self.trans[1] + dx1) * self.sign),
                      (self.loc[2] + dz,
                       self.loc[0] - (self.trans[1] - dx2) * self.sign),
                      (self.loc[2] + dz,
                       self.loc[0] + (self.trans[0] + dx1) * self.sign)],
                    dtype=np.float32)
      ls = LineCollection([mirror_segs, range_segs], linewidths=self._lw,
                  linestyles='solid', colors=['gray', self._cl])
    
    else: # vertical reflection, draw dashed rectangle only
      pass
    
    return ls


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
