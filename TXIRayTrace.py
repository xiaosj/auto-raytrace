import time
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from geometry import *
from optics import *


primary = np.array ([0., 0., 1.], dtype=np.float32)
PC2S  = Collimator('PC2S', (1.2500, 0.0, 731.145), 0.016, 0.055)
Src = CrissCrossSource((1.25, 0., 690.), PC2S.loc, 0.02, PC2S.iR*2)
M1K3  = FlatMirror('M1K3',
                   location=(1.2500, 0.0, 735.422), size=(0.02, 0.02, 1.0),
                   direction='x', A=-0.0098468, deltaA=(-0.00015, 0.00015),
                   translation=(-0.001, 0.001), incidentNorm=primary)
primary = M1K3.out
print(primary)
M2K3  = FlatMirror('M2K3',
                   location=(1.2184, 0.0, 737.022), size=(0.02, 0.02, 1.0),
                   direction='x', A=-0.0098468, deltaA=(-0.00015, 0.00015),
                   translation=(-0.001, 0.001), incidentNorm=primary)

primary = M2K3.out
print(primary)
PC1K3 = Collimator('PC1K3', (0.0, 0.0, 744.0), 0.008, 0.084)
PC1K3.setXYfromMirror(M2K3)
comp_list = [Src, PC2S, M1K3, M2K3, PC1K3]

fig, ax = plt.subplots(figsize=(7,4), dpi=100, facecolor='white')
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
for _ in range(5):
    ray = Src.getOneRay()
    ax.add_collection(LineCollection([ray], linewidths = 1, colors = 'blue'))

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
ax.set_title('TXI SXR')
plt.tight_layout()

plt.show()
