
import numpy as np

class BinaryTree:

	def __init__(self,data):
		self.data=data
		self.left=None
		self.right=None

	def add(self,data):
		if self.data==data:
			return
		if data<self.data:
			if self.left:
				self.left.add(data)
			else:
				self.left=BinaryTree(data)
		else:
			if self.right:
				self.right.add(data)
			else:
				self.right=BinaryTree(data)

	def search(self,val):
		if self.data==val:
			return True
		if self.data<val:
			if self.left:
				self.left.search(val)
			else:
				return False
		else:
			if self.right:
				self.right.search(val)
			else:
				return False

	def in_traverse(self):
		elements=[]
		if self.left:
			elements+=self.left.in_traverse()
		elements.append(self.data)
		if self.right:
			elements+=self.right.in_traverse()
		return elements

	def find_min(self):
		if self.left:
			self.left.find_min()
		else:
			return self.data

	def find_max(self):
		if self.right:
			self.right.find_min()
		else:
			return self.data

	def cal_sum(self):
		elements=self.in_traverse()
		return sum(elements)

	def post_traverse(self):
		elements=[]
		if self.left:
			elements+=self.left.post_traverse()
		if self.right:
			elements+=self.right.post_traverse()
		elements.append(self.data)
		return elements

	def pre_traverse(self):
		elements=[]
		elements.append(self.data)
		if self.left:
			elements+=self.left.pre_traverse()
		if self.right:
			elements+=self.right.pre_traverse()
		return elements


def build(elements):
	root=BinaryTree(elements[0])
	for i in range(1,len(elements)):
		root.add(elements[i])
	return root

tree=build(np.random.randint(100, size=10000000))

print(tree.in_traverse())







