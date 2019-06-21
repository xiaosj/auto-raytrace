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
M1K3  = FlatMirror('M1K3',
                   location=(1.2500, 0.0, 735.422), size=(0.02, 0.02, 1.0),
                   direction='x', A=-0.009, deltaA=(-0.00025, 0.00025),
                   translation=(-0.001, 0.001), incidentNorm=primary)
primary = M1K3.out
PC1K3 = Collimator('PC1K3', (0.0, 0.0, 744.000), 0.008, 0.084)
PC1K3.setXYfromMirror(M1K3)
comp_list = [PC2S, M1K3, PC1K3]
fig, ax = plt.subplots(figsize=(7,4), dpi=100, facecolor='white')
plt.ion()
for i in range(10):
  ax.clear()
  M1K3.A -= 0.002
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

  # set drawing range with padding
  zpad = 0.02
  dz = zmax - zmin
  zmin -= zpad * dz
  zmax += zpad * dz
  xpad = 0.02
  dx = xmax - xmin
  xmin -= xpad * dx
  xmax += xpad * dx
  ax.set_xlim(xmin=zmin, xmax=zmax)
  ax.set_ylim(ymin=xmin, ymax=xmax)

  ax.set_title('Step {:d}'.format(i))
  plt.tight_layout()
  fig.canvas.draw()
  fig.canvas.flush_events()
  plt.pause(0.001)
  time.sleep(0.3)

plt.show()
