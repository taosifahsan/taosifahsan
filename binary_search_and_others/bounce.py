import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import sys
import math

fig = plt.figure(figsize=(6,6))
# creating a subplot
ax1 = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
size=10
n=int(sys.argv[1])
G=-1000
dt=0.01
x, y =[None] * n ,[None] * n
vx, vy =[None] * n ,[None] * n
for i in range(0,n):
    x[i]=random.uniform(-size*0.8,size*0.8)*math.cos(random.uniform(0,2*np.pi))
    y[i]=random.uniform(-size*0.8,size*0.8)*math.sin(random.uniform(0,2*np.pi))
    vx[i] = 3*random.uniform(0, size) * math.cos(random.uniform(0, 2 * np.pi))
    vy[i] = 3*random.uniform(0, size) * math.sin(random.uniform(0, 2 * np.pi))


def animate(frame):

    global x,y,ax,ay,vx,vy,ax1, G

    ax1.clear()
    vx_n = vx.copy()
    vy_n = vy.copy()

    for i in range(0,n):

        #for j in range(0,n):
            #if (i==j):
                #continue
            #R = ((x[i]-x[j])**2+(y[i]-y[j])**2)**(0.5)
            #if (R<=0.5):
                #vx[i] = -vx_n[j]
                #vy[i] = -vy_n[j]

        if ((x[i]+ vx[i] * dt < -size)|(x[i] + vx[i] * dt> size)):
            vx[i] = -vx[i]
            x[i] += vx[i] * dt
            y[i] += vy[i] * dt
            ax1.plot(x[i], y[i], 'bo', markersize=10)
            continue
        if ((y[i]+ vy[i] * dt < -size)|(y[i]+vy[i] * dt > size)):
            vy[i] = -vy[i]
            x[i] += vx[i] * dt
            y[i] += vy[i] * dt
            ax1.plot(x[i], y[i], 'bo', markersize=10)
            continue

        vy[i]+=G*dt
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt

        ax1.plot(x[i], y[i],'bo',markersize=10)

    ax1.plot([-size, size], [size, size], linewidth=5)
    ax1.plot([-size, -size], [-size, size], linewidth=5)
    ax1.plot([size, -size], [-size, -size], linewidth=5)
    ax1.plot([size, size], [size, -size], linewidth=5)
    ax1.plot([size*1.2, -size*1.2],[size*1.2,-size*1.2],'ro',markersize=0.01)


ani = animation.FuncAnimation(fig, animate, interval=1, blit=False)
plt.show()