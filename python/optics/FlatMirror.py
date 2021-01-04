import numpy as np
from matplotlib.collections import LineCollection

from .geometry import *

class FlatMirror():
    """Class of a flat mirror.

    Args:
        name (str): mirror name.
        length, width, thickness: mirror dimensions.
        center: vector of nominal mirror center.
        nominalIn: nominal incident vector.
        orientation: mirror orientation: 'x+', 'x-', 'y+', 'y-'.
        A: nominal incident angle in rad.
        dA: (2,) rotation angle (-,+).
        trans: (2,) translation range (-,+).
    
    Attributes:
        xrefl (bool): True if reflection on X plane.
        sign: +/-1 to indicate the mirror orientation.
        norm: norm vector at nominal.
        norminalOut: nominal output vector
        _vertexes0: facility vertexes when mirror center at the origin and no rotation
        vertexes: vertexes of the mirror
    """
    _cl = 'red'  # color on drawing
    _lw = 1      # linewidth on drawing
    
    def __init__(self, name: str, length, width, thickness, 
                 center: Vector3, nominalIn: Vector3, orientation: str,
                 A, dA, trans):
        self.name = name
        self.half_length = length * 0.5
        self.half_width = width * 0.5
        self.thickness = thickness
        self.center = center
        self.nominalIn = nominalIn.normalized()
        self.nominalAx = np.arccos(self.nominalIn.x)
        self.A = A
        self.dA = dA
        self.trans = trans
        
        if orientation[0] == 'x' or orientation[0] == 'X':
            self.xrefl = True
        elif orientation[0] == 'y' or orientation[0] == 'Y':
            self.xrefl = False
        else:
            raise ValueError('Invalid orientation. Use only x+, x-, y+, or y-')

        if orientation[1] == '+':
            self.sign = 1
        elif  orientation[1] == '-':
            self.sign = -1
        else:
            raise ValueError('Invalid orientation. Use only x+, x-, y+, or y-')

        if self.xrefl:
            self._vertexes0 = [
                Vector3(0,  self.half_width, -self.half_length),
                Vector3(-self.thickness,  self.half_width, -self.half_length),
                Vector3(-self.thickness, -self.half_width, -self.half_length),
                Vector3(0, -self.half_width, -self.half_length),
                Vector3(0,  self.half_width,  self.half_length),
                Vector3(-self.thickness,  self.half_width, self.half_length),
                Vector3(-self.thickness, -self.half_width, self.half_length),
                Vector3(0, -self.half_width, self.half_length),
            ]
        else:
            self._vertexes0 = [
                Vector3(self.half_width, 0, -self.half_length),
                Vector3(-self.half_width, 0, -self.half_length),
                Vector3(-self.half_width, -self.thickness, -self.half_length),
                Vector3(self.half_width, -self.thickness, -self.half_length),
                Vector3(self.half_width, 0, self.half_length),
                Vector3(-self.half_width, 0, self.half_length),
                Vector3(-self.half_width, -self.thickness, self.half_length),
                Vector3(self.half_width, -self.thickness, self.half_length)
            ]
        
        self.norm, self.vertexes = self._calNormVertex(A)
        return

    def _calNormVertex(self, inA):
        """Calculate the normal vector and mirror vertexes"""
        if self.xrefl:
            vz = self.nominalIn.Ry(self.sign * inA)
            vx = vz.Ry(self.sign * np.pi / 2)
            vy = vz.cross(vx).normalized()
            norm = vx
            vertexes = [
                self.center + vy * self.half_width - vz * self.half_length,
                self.center + vy * self.half_width - vz * self.half_length - vx * self.sign * self.thickness,
                self.center - vy * self.half_width - vz * self.half_length - vx * self.sign * self.thickness,
                self.center - vy * self.half_width - vz * self.half_length,
                self.center + vy * self.half_width + vz * self.half_length,
                self.center + vy * self.half_width + vz * self.half_length - vx * self.sign * self.thickness,
                self.center - vy * self.half_width + vz * self.half_length - vx * self.sign * self.thickness,
                self.center - vy * self.half_width + vz * self.half_length
            ]
        else:
            vz = self.nominalIn.Rx(self.sign * inA)
            vy = vz.Rx(self.sign * np.pi / 2)
            vx = vz.cross(vy).normalized()
            norm = vy
            vertexes = [
                self.center + vx * self.half_width - vz * self.half_length,
                self.center - vx * self.half_width - vz * self.half_length,
                self.center - vx * self.half_width - vz * self.half_length - vy * self.sign * self.thickness,
                self.center + vx * self.half_width - vz * self.half_length - vy * self.sign * self.thickness,
                self.center + vx * self.half_width + vz * self.half_length,
                self.center - vx * self.half_width + vz * self.half_length,
                self.center - vx * self.half_width + vz * self.half_length - vy * self.sign * self.thickness,
                self.center + vx * self.half_width + vz * self.half_length - vy * self.sign * self.thickness
            ]
        return norm, vertexes

    # def _initSurfaces(self):
    #     # initialize mirror reflection and front surfaces on each dvision
    #     self.refl = np.zeros((self.ndA*self.ntrans, 6), dtype=np.float32)
    #     self.front = np.zeros_like(self.refl)
    #     for iA in range(self.ndA):
    #         A = self.A + self.dA[0] + (self.dA[1] - self.dA[0]) * iA / (self.ndA - 1)
    #     for iX in range(self.ntrans):
    #         trans = self.trans[0] + (self.trans[1] - self.trans[0]) * iX / (self.ntrans - 1)

    def setXYfromMirror(self, mirror):
        pass
        
    def drawZX(self):
        """ Draw component on the Z-X plane (horizontal)"""
        if(self.horizontal):  # horizontal reflection
        # mirror body
            rot = rot2D(self.A)
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
        # v0 = np.copy(self.loc)
        # n = np.copy(self.norm)
        # v0[0] += (self.trans[1] - self.trans[0]) * np.random.random() + self.trans[0] 
        # dA = (self.dA[1] - self.dA[0]) * np.random.random() + self.dA[0]
        # n = Ry(dA).dot(n)

        # p0 = ray[0]
        # u = VectorNormalize(ray[1] - p0)
        # w = v0 - p0
        # s = n.dot(w) / n.dot(u)

        # ps = p0 + s * u

        # zs = ps[2]
        # z0 = v0[2]
        # half_l = self.half_size[2]
        # nx = np.abs(n[0])
        # zmin = z0 - half_l * nx
        # zmax = z0 + half_l * nx

        # if zs >= zmin and zs <= zmax:
        #     refl_u = Reflection(u, n)
        #     output_ray = np.array([ps, ps + refl_u * 0.1])
        # else:
        #     output_ray = np.array([ps, ps + u])
        # return output_ray
        pass