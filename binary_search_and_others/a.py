import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import sys
import math

power=-2
fig = plt.figure(figsize=(6, 6))
# creating a subplot
ax1 = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
size = 10
n = int(sys.argv[1])
G = 1
dt = 0.5
a = 0.05
x, y = [None] * n, [None] * n
vx, vy = [None] * n, [None] * n
ax, ay = [0] * n, [0] * n
for i in range(0, n):
    x[i] = size*math.cos(i * 2 * math.pi / n)/2
    y[i] = size*math.sin(i * 2 * math.pi / n)/2
    vy[i] =  -x[i]
    vx[i] = y[i]


def animate(frame):
    global x, y, ax, ay, vx, vy, ax1, G
    ax1.clear()

    for i in range(0, n):
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt

        x_neg = (x[i] < -size * (1 - a))
        x_pos = (x[i] > size * (1 - a))
        y_neg = (y[i] < -size * (1 - a))
        y_pos = (y[i] > size * (1 - a))

        if (x_neg):
            x[i] = -size * (1 - a)
            vx[i] *= -1
        if (x_pos):
            x[i] = size * (1 - a)
            vx[i] *= -1
        if (y_neg):
            y[i] = -size * (1 - a)
            vy[i] *= -1
        if (y_pos):
            y[i] = size * (1 - a)
            vy[i] *= -1
        ax[i] = 0
        ay[i] = 0
        for j in range(0, n):
            if (i == j):
                continue
            R = ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** (0.5)
            if R < a*size*2:
                F = R*(a*size)**(power-2)
            else:
                F = R ** (power-1)
            ax[i] += (x[j] - x[i]) * G * F
            ay[i] += (y[j] - y[i]) * G * F

        vx[i] += ax[i] * dt
        vy[i] += ay[i] * dt

        ax1.plot(x[i], y[i], 'ro', markersize=10)

    ax1.plot([-size * 1.5, size * 1.5], [- size * 1.5, size * 1.5], 'ro', markersize=0.01)
    ax1.plot([-size, size], [size, size], 'b-', linewidth=5)
    ax1.plot([-size, -size], [-size, size], 'b-', linewidth=5)
    ax1.plot([size, -size], [-size, -size], 'b-', linewidth=5)
    ax1.plot([size, size], [size, -size], 'b-', linewidth=5)


ani = animation.FuncAnimation(fig, animate, interval=1, blit=False)
plt.show()
