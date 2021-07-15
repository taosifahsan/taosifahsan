import sys
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap




def zeta(s,n):
	sum=[0]*len(s)
	for r in range(n):
		sum+=(r+1)**(-s)
	return sum

i=(-1)**0.5
x=np.linspace(1,11,20)
y=np.linspace(-10,10,20)
x, y = np.meshgrid(x, y)

s=x+i*y
z=zeta(s, 10)-1

plt.style.use('dark_background')
colors = [	(0.0, 1.0, 1.0, 1.0),
			(0.0, 0.5, 1.0, 1.0),
			(0.0, 0.0, 1.0, 1.0)]  


cmap_name = 'my_list'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=20)

fig = plt.figure()
ax = fig.add_subplot(111)
strm=ax.streamplot(x,y,z.real,z.imag,
			color=np.log(abs(z))/np.log(10),
			linewidth=1,density=3,cmap=cm)
fig.colorbar(strm.lines)
plt.show()
