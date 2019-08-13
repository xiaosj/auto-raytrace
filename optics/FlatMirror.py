import numpy as np
from matplotlib.collections import LineCollection

import sys
sys.path.append('..')
import geometry as g

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
    self.A = A + np.arctan(incidentNorm[0] / incidentNorm[2]) 
    self.dA = np.array(deltaA, dtype=np.float32)
    if(direction == 'x' or direction == 'X'):
      self.horizontal = True
      self.norm = np.array([np.cos(self.A)*self.sign, 0., -np.abs(np.sin(self.A))], dtype=np.float32)
    elif(direction == 'y' or direction == 'Y'):
      self.horizontal = False
      self.norm = np.array([0., np.cos(self.A)*self.sign, -np.abs(np.sin(self.A))], dtype=np.float32)
    else:
      raise ('Wrong direction {:}.  Must be X or Y'.format(direction))
    self.trans = np.array(translation, dtype=np.float32)
    self.inp = g.VectorNormalize(incidentNorm)        # primary input  beam (normalized)
    self.out = g.Reflection(incidentNorm, self.norm)  # primary output beam (normalized)
    self.ndA = ndA
    self.ntrans = ntrans
    self._initSurfaces()


  def setA(self, newA):
    self.A = newA
    if(self.horizontal):
      self.norm = np.array([np.cos(self.A)*self.sign, 0., -np.abs(np.sin(self.A))], dtype=np.float32)
    else:
      self.norm = np.array([0., np.cos(self.A)*self.sign, -np.abs(np.sin(self.A))], dtype=np.float32)
    self.out = g.Reflection(self.inp, self.norm)


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
      rot = g.rot2D(self.A)
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
      #  ** this part needs to be fixed to take +/- dA **
      dz  = self.half_size[2] * np.cos(self.A - self.dA[1])
      dx1 = self.half_size[2] * np.sin(np.abs(self.A) + self.dA[1])
      dx2 = self.half_size[2] * np.sin(np.abs(self.A) - self.dA[1])
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

  def transport(self, ray):
    v0 = self.loc
    n = self.norm
    p0 = ray[0]
    u = g.VectorNormalize(ray[1] - p0)
    w = v0 - p0
    s = n.dot(w) / n.dot(u)

    ps = p0 + s * u

    zs = ps[2]
    z0 = v0[2]
    half_l = self.half_size[2]
    nx = np.abs(n[0])
    zmin = z0 - half_l * nx
    zmax = z0 + half_l * nx

    if zs >= zmin and zs <= zmax:
      refl_u = g.Reflection(u, n)
      output_ray = np.array([ps, ps + refl_u])
    else:
      output_ray = np.array([ps, ps + u])
    return output_ray