import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

class particles:

	def __init__(state, x=[],y=[],vx=[],vy=[],m=[],rad=[]):

		state.x=x
		state.y=y
		state.vx=vx
		state.vy=vy
		state.m=m
		state.rad=rad

	def add(state,x,y,vx,vy,m):
		state.x.append(x)
		state.y.append(y)
		state.vx.append(vx)
		state.vy.append(vy)
		state.m.append(m)
		state.rad.append(rad)

	def add_array(state,x,y,vx,v,m):
		state.x=state.x+x
		state.y=state.y+y
		state.vx=state.vx+vx
		state.vy=state.vy+vy
		state.m=state.m+m
		state.rad=state.rad+rad

	def acceleration(state):

		x=state.x
		y=state.y
		m=state.m
		rad=state.rad
		ax=[0]*len(x)
		ay=[0]*len(y)

		for i in range(len(x)):
			for j in range(len(y)):
				if j==i:
					continue

				rx,ry=x[j]-x[i],y[j]-y[i]
				r=(rx**2+ry**2)**0.5

				a=m[j]
				
				inside=(r<=rad[i]+rad[j])
				outside=1-inside

				term_x_in=a*rx
				term_x_out=a*rx/r**3

				term_y_in=a*ry
				term_y_out=a*ry/r**3

				ax[i]+=inside*term_x_in+outside*term_x_out
				ay[i]+=inside*term_y_in+outside*term_y_out

		return ax,ay

	def step(state,dt):

		ax,ay=state.acceleration()

		for i in range(len(state.x)):
			state.vx[i]+=ax[i]*dt
			state.vy[i]+=ay[i]*dt
			state.x[i]+=vx[i]*dt#+0.5*ax[i]*dt**2
			state.y[i]+=vy[i]*dt#+0.5*ay[i]*dt**2

	def momentum(state):
		px=0
		py=0
		for i in range(len(state.vx)):
			px+=state.m[i]*state.vx[i]
			py+=state.m[i]*state.vy[i]

		return px,py

plt.style.use('dark_background')

R=15
V=1
M=0.1

N=int(sys.argv[1])

dt=float(sys.argv[2])
G=10

theta=np.random.rand(N-1)*2*np.pi
Radius=np.random.rand(N-1)*R

x=Radius*np.cos(theta)
y=Radius*np.sin(theta)
rad=(np.random.rand(N)+1)*0.2


x=np.append(x,0)
y=np.append(y,0)

vx=[0]*N
vy=[0]*N
m=np.random.rand(N-1)*M


tot_mass=np.sum(m)
center_mass=100*M
m=np.append(m,center_mass)

for i in range(N-1):
	r=(x[i]**2+y[i]**2)*0.5
	v=(G*center_mass/r+G*tot_mass*r/R**2)**(0.5)

	vx[i]=-v*y[i]/r
	vy[i]= v*x[i]/r




curr_state=particles(x,y,vx,vy,m,rad)

fig=plt.figure("Gravity")

ax = fig.add_subplot(111, aspect='equal', autoscale_on=True,
                     xlim=(-2*R, 2*R), ylim=(-2*R, 2*R))
ax.grid()

line, = ax.plot([], [],'o',color= (0.2,1,0.1,0.5),markersize=5)

p_vec_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def init():
    line.set_data(curr_state.x, curr_state.y)
    p_vec_text.set_text(' ')
    return line, p_vec_text

def animate(i):
	px,py=curr_state.momentum()
	line.set_data(curr_state.x,curr_state.y)

	p_vec_text.set_text('$(v_x, v_y)$=(%.3f' %(px/tot_mass)+', %.3f)'%(py/tot_mass))
	curr_state.step(dt)
	plt.draw()
	return line, p_vec_text

ani = animation.FuncAnimation(fig, animate, frames=6000, interval=1, blit=True, init_func=init)

plt.show()
		