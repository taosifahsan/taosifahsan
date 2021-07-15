import numpy as np
import matplotlib.pyplot as plt
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
		F= G*self.mass*b.mass/r**2
		return F*rx/r
	#y-component
	def force_y(self,b):
		G=1
		ry=self.py-b.py
		r=self.distance(b)
		F= G*self.mass*b.mass/r**2
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
			x=self.b
			if self.b.inside(self.nw.q):
				self.nw.insert(x)
			elif self.b.inside(self.ne.q):
				self.ne.insert(x)
			elif self.b.inside(self.sw.q):
				self.sw.insert(x)
			else:
				self.se.insert(x)
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
				
				plt.plot([self.b.px,b_n.px],[self.b.py,b_n.py], color=(0,0,1,0.7),markersize=1)
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
				
				plt.plot([self.b.px,b_n.px],[self.b.py,b_n.py],color=(0,0,1,0.4),markersize=1)
				return self.b.force_x(b_n)
			#otherwise
			else:
				
				#run the procedure recursively on
				#each of the current node's children
				force_nw=self.nw.updateForce_x(b_n)
				print(force_nw)
				force_ne=self.ne.updateForce_x(b_n)
				print(force_ne)
				force_sw=self.sw.updateForce_x(b_n)
				print(force_sw)
				force_se=self.se.updateForce_x(b_n)
				print(force_se)
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
				elements.append(self.b)
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
			elements.append(self.q)
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
#--------------------testing-the-methods-----------------------
#--------------------------------------------------------------


plt.style.use('dark_background')
q=quad(-0.5, -0.5, 1)
N=100
px=np.random.rand(2)*0.5
py=-np.random.rand(2)*0.5
m=[1]*len(px)
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
bodies=build_bodies(px,py,m)
root=build_Tree(bodies,q)
quads=root.read_quad()
F=root.updateForce_x(bodies[0])
for i in range(len(quads)):
	x,y=quads[i].draw()
	ax.plot(x,y,'-',color=(0,1,1,0.4),markersize=1)
ax.plot(px,py,'o',color=(1,0,0,0.5),markersize=3)
ax.text(-0.2,0.55,'number of qudrants = '+str(len(quads)))
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(-0.6,0.6)
ax.set_ylim(-0.6,0.6)
print(F)
plt.show()
















































