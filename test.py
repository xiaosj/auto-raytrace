"""
Ray trace automation
simple loop version for test
@author: xiaosj
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from geometry import *
from optics import *

# test case
primary = np.array([0., 0., 1.], dtype=np.float32)
PC2S  = Collimator('PC2S', (1.2500, 0.0, 731.145), 0.016, 0.055)
Src = CrissCrossSource((1.25, 0., 690.), PC2S.loc, 0.02, PC2S.iR*2)
M1K3  = FlatMirror('M1K3',
                   location=(1.2500, 0.0, 735.422), size=(0.02, 0.02, 1.0),
                   direction='x', A=-0.009, deltaA=(-0.00025, 0.00025),
                   translation=(-0.001, 0.001), incidentNorm=primary)
primary = M1K3.out
PC1K3 = Collimator('PC1K3', (1.25, 0.0, 744.000), 0.008, 0.084)
#PC1K3 = Collimator('PC1K3', (0.0, 0.0, 744.000), 0.008, 0.084)
PC1K3.setXYfromMirror(M1K3)
comp_list = [Src, PC2S, M1K3, PC1K3]

fig, ax = plt.subplots(figsize=(7,4), dpi=100, facecolor='white')
for i in range(1):
  ax.clear()
  M1K3.setA(M1K3.A - 0.002)
  PC1K3.setXYfromMirror(M1K3)
  xmin =  np.inf
  xmax = -np.inf
  zmin =  np.inf
  zmax = -np.inf
  paths = []
  for comp in comp_list:
    ax.add_collection(comp.drawZX())
    if(xmin > comp.draw_min[0]):  xmin = comp.draw_min[0]
    if(xmax < comp.draw_max[0]):  xmax = comp.draw_max[0]
    if(zmin > comp.draw_min[1]):  zmin = comp.draw_min[1]
    if(zmax < comp.draw_max[1]):  zmax = comp.draw_max[1]

  # draw 5 random rays
  for ir in range(5):
    ray = Src.getOneRay()
    # ray = np.array([[1.25, 0, 690], [1.25, 0, 731]])
    print('Input ray', ir, ': ', ray)
    ray_p0 = [ray[0,2], ray[0,0]]
    ray_p1 = [ray[1,2], ray[1,0]]
    ax.add_collection(LineCollection([
          [ray_p0, ray_p1]
          ], linewidths = 0.5, colors = 'blue'))

    out_ray = M1K3.transport(ray)
    print('Output ray', ir, ': ', out_ray)
    outray_p0 = [out_ray[0,2], out_ray[0,0]]
    outray_p1 = [out_ray[1,2], out_ray[1,0]]
    ax.add_collection(LineCollection([
           [ray_p1, outray_p0],
           [outray_p0, outray_p1]
           ], linewidths = 0.5, colors = 'blue'))
    
    out_ray = PC1K3.transport(out_ray)
    print('Output ray', ir, ': ', out_ray)
    ray_p1 = outray_p1
    outray_p0 = [out_ray[0,2], out_ray[0,0]]
    outray_p1 = [out_ray[1,2], out_ray[1,0]]
    ax.add_collection(LineCollection([
          [ray_p1, outray_p0],
          [outray_p0, outray_p1]
          ], linewidths = 0.5, colors = 'blue'))

  # set drawing range with padding
  zpad = 0.02
  dz = zmax - zmin
  zmin -= zpad * dz
  zmax += zpad * dz
  xpad = 0.02
  dx = xmax - xmin
  xmin -= xpad * dx
  xmax += xpad * dx
  ax.set_xlim(left=zmin, right=zmax)
  ax.set_ylim(bottom=xmin, top=xmax)

  ax.set_title('Step {:d}'.format(i))
  plt.tight_layout()
  fig.canvas.draw()
  fig.canvas.flush_events()
  plt.pause(0.001)
  time.sleep(0.8)
  
  plt.show()