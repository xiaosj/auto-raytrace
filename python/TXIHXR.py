import time
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from optics import *


primary = np.array ([0., 0., 1.], dtype=np.float32)
PC1H  = Collimator('PC1H', (-1.2500, 0.0, 735.211), 0.008, 0.055)
Src = CrissCrossSource((-1.25, 0., 690.), PC1H.loc, 0.02, PC1H.iR*2)
M1LO  = FlatMirror('M1LO',
                   location=(-1.2500, 0.0, 740.000), size=(0.02, 0.02, 1.0),
                   direction='x', A=-0.0098468, deltaA=(-0.00015, 0.00015),
                   translation=(-0.001, 0.001), incidentNorm=primary)
primary = M1LO.out
print(primary)
M1L1  = FlatMirror('M1L1',
                   location=(-1.227, 0.0, 741.600), size=(0.02, 0.02, 1.0),
                   direction='x', A=-0.0098468, deltaA=(-0.00015, 0.00015),
                   translation=(-0.001, 0.001), incidentNorm=primary)

primary = M1L1.out
print(primary)
PC1L1 = Collimator('PC1L1', (-1.114, 0.0, 745.621), 0.008, 0.084)
PC1L1.setXYfromMirror(M1L1)
PC2L1 = Collimator('PC2L1', (-1.00, 0.0, 749.616), 0.0145, 0.084)
comp_list = [Src, PC1H, M1LO, M1L1, PC1L1, PC2L1]
transport_list = [M1LO, M1L1, PC1L1, PC2L1]

fig, ax = plt.subplots(figsize=(7,5), dpi=100, facecolor='white')
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

zmin = 730.0
# draw 5 random rays
for ir in range(500):
    # generate 1 ray
    ray = Src.getOneRay()
#     print('Input ray', ir, ': ', ray)
    ray_p0 = [ray[0,2], ray[0,0]]
    ray_p1 = [ray[1,2], ray[1,0]]
    ax.add_collection(LineCollection([
          [ray_p0, ray_p1]
          ], linewidths = 0.5, colors = 'blue'))

    out_ray = M1LO.transport(ray)
#     print('Output ray', ir, ': ', out_ray)
    outray_p0 = [out_ray[0,2], out_ray[0,0]]
    outray_p1 = [out_ray[1,2], out_ray[1,0]]
    ax.add_collection(LineCollection([
           [ray_p1, outray_p0],
           [outray_p0, outray_p1]
           ], linewidths = 0.5, colors = 'blue')) 

    out_ray = M1L1.transport(out_ray)
#     print('Output ray', ir, ': ', out_ray)
    ray_p1 = outray_p1
    outray_p0 = [out_ray[0,2], out_ray[0,0]]
    outray_p1 = [out_ray[1,2], out_ray[1,0]]
    ax.add_collection(LineCollection([
           [ray_p1, outray_p0],
           [outray_p0, outray_p1]
           ], linewidths = 0.5, colors = 'blue')) 

    out_ray = PC1L1.transport(out_ray)
#     print('Output ray', ir, ': ', out_ray)
    ray_p1 = outray_p1
    outray_p0 = [out_ray[0,2], out_ray[0,0]]
    outray_p1 = [out_ray[1,2], out_ray[1,0]]
    ax.add_collection(LineCollection([
          [ray_p1, outray_p0],
          [outray_p0, outray_p1]
          ], linewidths = 0.5, colors = 'blue'))
          
    out_ray = PC2L1.transport(out_ray)
    #print('Output ray', ir, ': ', out_ray)
    ray_p1 = outray_p1
    outray_p0 = [out_ray[0,2], out_ray[0,0]]
    outray_p1 = [out_ray[1,2], out_ray[1,0]]
    ax.add_collection(LineCollection([
          [ray_p1, outray_p0],
          [outray_p0, outray_p1]
          ], linewidths = 0.5, colors = 'blue'))

    # transport
    # for comp in comp_list:
    #     out_ray = comp.transport(ray)

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
ax.set_title('TXI HXR')
plt.tight_layout()

plt.show()