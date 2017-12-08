from Tree_search cimport Node
import numpy as np
from Heuristic cimport score
ctypedef LONG long long int


cdef max_node(*args):
	cdef Node curr_max
	curr_max = args[0]
	for node in args[1:]:
		if node.score > curr_max.score:
			curr_max = node
	return curr_max

cdef min_node(*args):
	curr_min = args[0]
	for node in args[1:]
		if node.score < curr_min.score:curr_min = node
	return curr_min

cdef class cache:
	def __init__():
		self.cache = []
	def refresh():
		self.cache = []
	def add_Node(node):
		cache.append(node)
	def check(node):
		return node in cache
	

cdef class Node:
    def __init__(self, np.ndarray board, parent, cdef int depth, cdef int score=0)

	self.parent = parent
	self.board = board
        self.subnodes = []
        self.score = score
        self.depth = depth

    def sort_subnodes(self,func=score):
        return sorted(self.subnodes, key=func)


    def add_subnode(self,node, sort=True):
        self.subnodes.append(node)
        if sort:
            self.subnodes = self.sort_subnodes()
        


cdef full_alpha_beta(cdef Node node, cdef Node alpha, cdef Node beta, cdef int curr_depth, cdef int max_depth,
		cdef bool maximising):
	if depth == max_depth:
		if not cache.check(node):
			node.score = score(node)
		return node
	cdef Node value
	elif maxmising:
	 for subnode in node.subnodes:
		value  = Node(None, None, None, float("inf"))
		value = max_node(value, full_alpha_beta_tree_search((alpha, beta, subnode, depth + 1, max_depth, False))		
		if beta <= alpha:
			break
	 node.score = value
	 return value

	elif not maxmising:
		next_layer = node.subnodes
	 for subnode in next_layer:
		value  = Node(None, None, None, float("inf"))
		value = min_node(value, full_alpha_beta_tree_search((alpha, beta, subnode, depth + 1, max_depth, True))		
		if beta <= alpha:
			break
	node.score = value
	return value


cdef best_alpha_beta(node, LONG alpha, LONG beta, int curr_depth, int max_depth,
		bool maximising, int num_best_nodes):
	if depth == max_depth:
		Node.score = score(Node)
		return Node
	node.sort_subnodes()
	elif maxmising:
		next_layer = node.subnodes[:num_best_nodes]
	 for subnode in next_layer:
		value  = Node(None, None, None, - float("inf"))
		value = max_node(value, full_alpha_beta_tree_search((alpha, beta, subnode, depth + 1, max_depth, False))		
		
		if beta <= alpha:
			break
	 node.score=value
	 return value
	elif not maxmising:
		next_layer = node.subnodes[-1:len(node.subnodes) - num_best_nodes:-1]
	 for subnode in next_layer:
		value  = Node(None, None, None, float("inf"))
		value = min_node(value, full_alpha_beta_tree_search((alpha, beta, subnode, depth + 1, max_depth, True))		
		if beta <= alpha:
	 	 break
	 node.score = value
	 return value


