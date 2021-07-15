import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#interaction_force
def force(r):
	r_0=0.01
	inside=(r<=r_0)
	G=0.1
	F_out=G/r**2
	F_in=G*r/r_0**2
	return (not inside)*F_out+(inside)*F_in
#--------------------------------------------------------------
#-----------------------objects--------------------------------
#--------------------------------------------------------------
#qudrants of space: the square cells
class quad:
	def __init__(self,pos_x,pos_y,length):
		self.pos_x=pos_x
		self.pos_y=pos_y
		self.length=length
	#returns if a position is in the quadrant
	def contains(self,x,y):
		t_x=(self.pos_x<=x)*(x<self.pos_x+self.length)
		t_y=(self.pos_y<=y)*(y<self.pos_y+self.length)
		return (t_x*t_y)
	#creates a mini quadrant in northwest corner
	def NW(self):
		x=self.pos_x
		y=self.pos_y
		a=self.length
		model=quad(x,y+a/2,a/2)
		return model
	#creates a mini quadrant in northeast corner
	def NE(self):
		x=self.pos_x
		y=self.pos_y
		a=self.length
		model=quad(x+a/2,y+a/2,a/2)
		return model
	#creates a mini quadrant in southwest corner
	def SW(self):
		x=self.pos_x
		y=self.pos_y
		a=self.length
		model=quad(x,y,a/2)
		return model
	#creates a mini quadrant in southeast corner
	def SE(self):
		x=self.pos_x
		y=self.pos_y
		a=self.length
		model=quad(x+a/2,y,a/2)
		return model
	#returns co-ordinates to draw a quadrant
	def draw(self):
		x_0=self.pos_x
		y_0=self.pos_y
		a=self.length

		x=[x_0,x_0+a,x_0+a,x_0,x_0]
		y=[y_0,y_0,y_0+a,y_0+a,y_0]

		return x,y
#body: position and mass
class body:
	def __init__(self,px,py,mass):
		self.px=px
		self.py=py
		self.mass=mass
	#returns if body is in a qudrant
	def inside(self,q):
		return q.contains(self.px,self.py)
	#replaces two bodies with their COM and total mass
	def add(self, b):
		M=self.mass+b.mass
		pX=((self.px)*(self.mass)+(b.px)*(b.mass))/M
		pY=((self.py)*(self.mass)+(b.py)*(b.mass))/M
		return body(pX,pY,M)
	#returns the distance of two bodies
	def distance(self,b):
		return ((self.px-b.px)**2+(self.py-b.py)**2)**0.5
	#returns force between two bodies
	#x-component
	def force_x(self,b):
		G=1
		rx=self.px-b.px
		r=self.distance(b)
		F= self.mass*b.mass*force(r)
		return F*rx/r
	#y-component
	def force_y(self,b):
		G=1
		ry=self.py-b.py
		r=self.distance(b)
		F= self.mass*b.mass*force(r)
		return F*ry/r
#Tree:  COM, total mass and square cell COM is in
#and the trees and nodes underneath it
class BHTree: 
	def __init__(self, b, q):
		self.b=b
		self.q=q
		self.nw=None
		self.ne=None
		self.sw=None
		self.se=None
	#returns if a node has childs
	def internal(self):
		return self.nw or self.ne or self.sw or self.se
	#inserts a body in the a node of the Tree
	def insert(self,b_n):
		#if node does not contain a body, put the new body
		if not self.b:
			self.b=b_n
			return 
		#if node is an internal node,
		if self.internal():
			#update the COM and total mass
			self.b=self.b.add(b_n)
			#recursively insert the body
			if b_n.inside(self.nw.q):
				self.nw.insert(b_n)
			elif b_n.inside(self.ne.q):
				self.ne.insert(b_n)
			elif b_n.inside(self.sw.q):
				self.sw.insert(b_n)
			else:
				self.se.insert(b_n)
		#if node is an external node
		else: 
			#subdivide the region further
			self.nw=BHTree(None,self.q.NW())
			self.ne=BHTree(None,self.q.NE())
			self.sw=BHTree(None,self.q.SW())
			self.se=BHTree(None,self.q.SE())
			#recursively insert both bodies
			#previous body
			if self.b.inside(self.nw.q):
				self.nw.insert(self.b)
			elif self.b.inside(self.ne.q):
				self.ne.insert(self.b)
			elif self.b.inside(self.sw.q):
				self.sw.insert(self.b)
			else:
				self.se.insert(self.b)
			#new body
			if b_n.inside(self.nw.q):
				self.nw.insert(b_n)
			elif b_n.inside(self.ne.q):
				self.ne.insert(b_n)
			elif b_n.inside(self.sw.q):
				self.sw.insert(b_n)
			else:
				self.se.insert(b_n)
			self.b=self.b.add(b_n)
	#calculates total force on a body 
	#x-component
	def updateForce_x(self,b_n):
		theta=0.5
		#if there is no body in node
		if not self.b:
			#then there is no force from the node
			return 0
		#if the current node is an external node
		if not self.internal():
			#and it is not the body
			if self.b==b_n:
				return 0
			#calculate the force exerted by the current node
			#on body, and add this amount to body's net force
			else:
				return self.b.force_x(b_n)
		#otherwise
		else:
			#calculate the ratio s/d
			d=self.b.distance(b_n)
			s=self.q.length
			#if s/d<theta
			if s/d<=theta:
				#treat this internal node as a single body,
				#and calculate the force it exerts on given
				#body, and add this amount to body's net force
				return self.b.force_x(b_n)
			#otherwise
			else:
				#run the procedure recursively on
				#each of the current node's children
				force_nw=self.nw.updateForce_x(b_n)
				force_ne=self.ne.updateForce_x(b_n)
				force_sw=self.sw.updateForce_x(b_n)
				force_se=self.se.updateForce_x(b_n)
				return force_nw+force_ne+force_sw+force_se
	#y-component
	#same algorithm as x-component
	def updateForce_y(self,b_n):
		theta=0.5
		if not self.b:
			return 0
		if not self.internal():
			if self.b==b_n:
				return 0
			else:
				return self.b.force_y(b_n)
		else:
			d=self.b.distance(b_n)
			s=self.q.length
			if s/d<=theta:
				return self.b.force_y(b_n)
			else:
				force_nw=self.nw.updateForce_y(b_n)
				force_ne=self.ne.updateForce_y(b_n)
				force_sw=self.sw.updateForce_y(b_n)
				force_se=self.se.updateForce_y(b_n)
				return force_nw+force_ne+force_sw+force_se
	#returns the array of bodies from the tree
	def read(self):
		elements=[]
		#if the node is external and it has a body
		#add that body to array
		if not self.internal():
			if self.b:
				elements=np.append(elements,self.b)
		#if there are further childrens beneath 
		#the node, recursively add the associated arrays
		#with trees to the main array
		else:
			if self.nw:
				elements+=self.nw.read()
			if self.ne:
				elements+=self.ne.read()
			if self.sw:
				elements+=self.sw.read()
			if self.se:
				elements+=self.se.read()
		return elements
	#returns the array of quads from the tree
	def read_quad(self):
		elements=[]
		#if the node is external
		#add that body to array
		if not self.internal():
			elements=np.append(elements,self.q)
		#if there are further childrens beneath 
		#the node, recursively add the associated arrays
		#with trees to the main array
		else:
			if self.nw:
				elements+=self.nw.read_quad()
			if self.ne:
				elements+=self.ne.read_quad()
			if self.sw:
				elements+=self.sw.read_quad()
			if self.se:
				elements+=self.se.read_quad()
		return elements
#--------------------------------------------------------------
#-----------------------methods--------------------------------
#--------------------------------------------------------------
#To build an array of body object from position and mass array
def build_bodies(px,py,mass):
	bodies=[None]*(len(px))
	for i in range(len(px)):
		bodies[i]=body(px[i], py[i], mass[i])
	return bodies
#To build Tree from a body objects
def build_Tree(bodies,q_r):
	root=BHTree(bodies[0], q_r)
	for i in range(1,len(bodies)):
		if bodies[i].inside(q_r):
			root.insert(bodies[i])
	return root
#To get position and mass array from body array
def read_bodies(bodies):
	p_x=[None]*len(bodies)
	p_y=[None]*len(bodies)
	m=[None]*len(bodies)
	for i in range(len(bodies)):
		p_x[i]=bodies[i].px
		p_y[i]=bodies[i].py
		m[i]=bodies[i].mass
	return p_x,p_y,m
#--------------------------------------------------------------
#-------------------------animation----------------------------
#--------------------------------------------------------------
class particles:
	def __init__(self, x=[],y=[],vx=[],vy=[],m=[]):
		self.x=x
		self.y=y
		self.vx=vx
		self.vy=vy
		self.m=m
	def acceleration(self):
		bodies=build_bodies(self.x,self.y,self.m)
		q_r=quad(-0.5,-0.5,1)
		tree=build_Tree(bodies,q_r)
		ax=[0]*len(self.x)
		ay=[0]*len(self.x)
		for i in range(len(self.x)):
			ax[i]=tree.updateForce_x(bodies[i])/m[i]
			ay[i]=tree.updateForce_y(bodies[i])/m[i]
		return ax,ay
	def step(self,dt):
		ax,ay=self.acceleration()
		for i in range(len(self.x)):
			#predicted_x=self.x[i]+self.vx[i]*dt
			#predicted_y=self.y[i]+self.vy[i]*dt
			#inside_x=(-0.5<predicted_x)&(predicted_x<0.5)
			#inside_y=(-0.5<predicted_y)&(predicted_y<0.5)
			#outside_x=1-inside_x
			#outside_y=1-inside_y
			pred_vx=self.vx[i]+ax[i]*dt
			pred_vy=self.vy[i]+ay[i]*dt
			self.vx[i]=(pred_vx)#*inside_x-self.vx[i]*outside_x
			self.vy[i]=(pred_vy)#*inside_y-self.vy[i]*outside_y
			self.x[i]+=vx[i]*dt#+0.5*ax[i]*dt**2
			self.y[i]+=vy[i]*dt#+0.5*ay[i]*dt**2

plt.style.use('dark_background')

N=50
theta=np.random.rand(N)*2*np.pi
r=0.5*np.random.rand(N)
x=r*np.cos(theta)
y=r*np.sin(theta)
vx=[0]*N
vy=[0]*N
m=np.random.rand(N)

curr_self=particles()
curr_self.x=x
curr_self.y=y
curr_self.vx=vx
curr_self.vy=vy
curr_self.m=m

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
particle_animation, = ax.plot([], [],'o',markersize=10,color=(1,0,0,0.5))


def init():
    particle_animation.set_data([], [])
    return particle_animation,

dt=0.001
def animate(i):
	particle_animation.set_data(curr_self.x,curr_self.y)
	curr_self.step(dt)
	return particle_animation,

ax.set_xlim(-0.5,0.5)
ax.set_ylim(-0.5,0.5)

ani = animation.FuncAnimation(fig, animate, frames=6000, interval=1, blit=True, init_func=init)
plt.show()







