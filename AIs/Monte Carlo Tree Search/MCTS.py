import numpy as np
import random
import math

class tree
	class State:
			def __init__(self,t=0,n=0):
				# t = total value of state
				# n = number of visits
				# t/n = average value of the state
				self.t = t
				self.n = n
				self.tree = self.tree.Expand_Tree()

			def UCB1(self,parent_node,C=2):
				assert type(parent_node) == state
				return (t/n)+C*(math.sqrt(math.log(parent_node.n/self.n)))



	def __init__():

	def add_children():
		self.tshildren

	def backprop():