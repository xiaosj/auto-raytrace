import time
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

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
PC1K3 = Collimator('PC1K3', (1.25, 0.0, 744.000), 0.008, 0.084)
#PC1K3 = Collimator('PC1K3', (0.0, 0.0, 744.0), 0.008, 0.084) NORMAL COLLIMATOR SIZE
PC1K3.setXYfromMirror(M2K3)
PC2K3 = Collimator('PC2K3', (0.687, 0.0, 750.503), 0.0145, 0.084)
comp_list = [Src, PC2S, M1K3, M2K3, PC1K3, PC2K3]
transport_list = [M1K3, M2K3, PC1K3, PC2K3]

np.random.seed(1)

fig, ax = plt.subplots(figsize=(10,5), dpi=100, facecolor='white')
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
for ir in range(200):
    # generate 1 ray
    ray = Src.getOneRay()
#     print('Input ray', ir, ': ', ray)
    ray_p0 = [ray[0,2], ray[0,0]]
    ray_p1 = [ray[1,2], ray[1,0]]
    ax.add_collection(LineCollection([
          [ray_p0, ray_p1]
          ], linewidths = 0.5, colors = 'blue'))

    out_ray = M1K3.transport(ray)
#     print('Output ray', ir, ': ', out_ray)
    outray_p0 = [out_ray[0,2], out_ray[0,0]]
    outray_p1 = [out_ray[1,2], out_ray[1,0]]
    ax.add_collection(LineCollection([
           [ray_p1, outray_p0],
           [outray_p0, outray_p1]
           ], linewidths = 0.5, colors = 'blue')) 

    out_ray = M2K3.transport(out_ray)
#     print('Output ray', ir, ': ', out_ray)
    ray_p1 = outray_p1
    outray_p0 = [out_ray[0,2], out_ray[0,0]]
    outray_p1 = [out_ray[1,2], out_ray[1,0]]
    ax.add_collection(LineCollection([
           [ray_p1, outray_p0],
           [outray_p0, outray_p1]
           ], linewidths = 0.5, colors = 'blue')) 

    out_ray = PC1K3.transport(out_ray)
#     print('Output ray', ir, ': ', out_ray)
    ray_p1 = outray_p1
    outray_p0 = [out_ray[0,2], out_ray[0,0]]
    outray_p1 = [out_ray[1,2], out_ray[1,0]]
    ax.add_collection(LineCollection([
          [ray_p1, outray_p0],
          [outray_p0, outray_p1]
          ], linewidths = 0.5, colors = 'blue'))
          
    out_ray = PC2K3.transport(out_ray)
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
ax.set_title('TXI SXR')
plt.tight_layout()

plt.show()
