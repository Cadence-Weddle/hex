from Tree_search cimport Node
from Heuristic import score
typedef LONG long long int


cdef max_node(*args):
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



cdef class Node:
    def __init__(self, board, parent, depth, score=None):
        Node self.parent
	float score
	int depth
	
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
        


cdef full_alpha_beta(node, LONG alpha, LONG beta, int curr_depth, int max_depth,
		maximising):
	if depth == max_depth:
		Node.score = score(Node.board)
		return Node

	elif maxmising:
		next_layer = node.subnodes
	 for subnode in next_layer:
		value  = Node(None, None, None, -99999999)
		value = max_node(value, full_alpha_beta_tree_search((alpha, beta, subnode, depth + 1, max_depth, False))		
		if beta <= alpha:
			break
	 return value
	elif not maxmising:
		next_layer = node.subnodes
	 for subnode in next_layer:
		value  = Node(None, None, None, 99999999)
		value = min_node(value, full_alpha_beta_tree_search((alpha, beta, subnode, depth + 1, max_depth, True))		
		if beta <= alpha:
			break
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
		value  = Node(None, None, None, -99999999)
		value = max_node(value, full_alpha_beta_tree_search((alpha, beta, subnode, depth + 1, max_depth, False))		
		if beta <= alpha:
			break
	 return value
	elif not maxmising:
		next_layer = node.subnodes[-1:len(node.subnodes) - num_best_nodes:-1]
	 for subnode in next_layer:
		value  = Node(None, None, None, 99999999)
		value = min_node(value, full_alpha_beta_tree_search((alpha, beta, subnode, depth + 1, max_depth, True))		
		if beta <= alpha:
			break
	return value


