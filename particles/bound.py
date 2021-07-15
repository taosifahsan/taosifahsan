import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

class particles:

	def __init__(state, x=[],y=[],vx=[],vy=[],box=[]):

		state.x=x
		state.y=y
		state.vx=vx
		state.vy=vy
		state.box=box

	def add(state,x,y,vx,vy,m):
		state.x.append(x)
		state.y.append(y)
		state.vx.append(vx)
		state.vy.append(vy)
		state.box.append(box)

	def step(state,g,dt):

		x_min=box[0]
		x_max=box[1]
		y_min=box[2]
		y_max=box[3]

		for i in range(len(state.x)):

			inside_x=(x_min<state.x[i]+state.vx[i]*dt)&(state.x[i]+state.vx[i]*dt<x_max)
			inside_y=(y_min<state.y[i]+state.vy[i]*dt)&(state.y[i]+state.vy[i]*dt<y_max)

			outside_x=1-inside_x
			outside_y=1-inside_y

			state.vx[i]=(2*inside_x-1)*state.vx[i]
			state.vy[i]=(state.vy[i]-g*dt)*inside_y+(-1)*state.vy[i]*outside_y
			

			state.x[i]+=state.vx[i]*dt
			state.y[i]+=state.vy[i]*dt

	def v_ms(state):
		sum=0
		for i in range(len(state.vx)):
			sum+=state.vx[i]**2+state.vy[i]**2
		return sum/len(state.vx)

plt.style.use('dark_background')

box=[-5,5,-5,5]
N=int(sys.argv[1])
dt=float(sys.argv[2])
v_x=0
v_y=0
g=9.81


curr_state=particles()
curr_state.box=box
curr_state.vx=(2*np.random.rand(N)-1)*v_x
curr_state.vy=(2*np.random.rand(N)-1)*v_y

beta=curr_state.v_ms()/(2*g)

curr_state.x=np.random.rand(N)*(box[1]-box[0])+box[0]
curr_state.y=np.random.rand(N)*(box[3]-box[2])+box[2]
#curr_state.y=np.random.exponential(beta,N)+box[2]

for i in range(N):
	if curr_state.y[i]>=box[3]:
		curr_state.y[i]=box[3]*0.99

fact2=1.1
fig=plt.figure("Bound")
ax = fig.add_subplot(111, aspect='equal', autoscale_on=True, 
					xlim=(box[0]*fact2, box[1]*fact2), ylim=(box[2]*fact2, box[3]*fact2))

fact1=1.04
boundary_array_x=[box[0]*fact1,box[1]*fact1,box[1]*fact1,box[0]*fact1,box[0]*fact1]
boundary_array_y=[box[2]*fact1,box[2]*fact1,box[3]*fact1,box[3]*fact1,box[2]*fact1]
ax.plot(boundary_array_x,boundary_array_y, lw=7,color=(0.2,0.2,0.2,0.5))
temp=ax.text(box[0],box[1], ' ', color=(1,1,1,0.5))

particle_animation, = ax.plot([], [],'o',markersize=2,color=(1,0,0,0.5))

def init():
    particle_animation.set_data([], [])
    temp.set_text(' ')
    return particle_animation, temp,

def animate(i):
	particle_animation.set_data(curr_state.x,curr_state.y)
	temp.set_text('T=%.1f'%curr_state.v_ms())
	curr_state.step(g, dt)
	return particle_animation, temp,

ani = animation.FuncAnimation(fig, animate, frames=6000, interval=1, blit=True, init_func=init)
plt.axis('off')
plt.show()