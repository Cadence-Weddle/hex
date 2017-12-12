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
	

cpdef class Node:
    def __init__(self, game, parent, cdef int depth, cdef float score=0, cdef string get_moves="get_moves", cdef string make_move="make_moves")
	self.parent = parent
	self.game = game
        self.subnodes = []
        self.score = score
        self.depth = depth
	self.make_move = make_move
	self.get_moves = get_moves
#Checking inputs
	try:		
		game = self.game
		assert type(parent) in (Node, None)
		getattr(game, self.get_moves)
		getattr(game, self.make_move)
	except:
		raise TypeError

		
    def sort_subnodes(self,func=score):
        return sorted(self.subnodes, key=func)


    def add_subnode(self,node, sort=True):
        self.subnodes.append(node)
        if sort:
            self.subnodes = self.sort_subnodes()
    
    def expand(self):
	game = self.game
	moves = getattr(game, self.get_moves)()
	for move in moves:
		self.add_subnode(Node(getattr(game, self.make_move)(move), self, self.depth + 1, get_moves=self.get_moves, make_move=self.make_move)
	return self.subnodes




cpdef class Tree():

    def __init__(self, game, player, other_player, depth=0):
        self.board = board
        self.turn_conversion = {0 : -1, 1 : 1}
        converted_players={player : 1, other_player : -1, 0 : 0}
        if other_player == 1:
            self.player_is_first = False
        else:
            self.player_is_first = True
        self.board = self.convert_board(board, converted_players)
        self.depth = 0
        self.root_node = Node(self.board, parent=None, depth=0)
        self.terminal_nodes = []
        while  self.depth <= depth:
            self.next_layer()

    def next_layer(self):
        nodes = []
        for node in self.terminal_nodes:
            nodes.append(self.expand_node(node))
        nodes = [i for i in iter_flatten(nodes)]
        self.terminal_nodes = nodes
        self.depth += 1
        return list(set(nodes))

    def expand_node(self, node, expansion_size=121):
        board = node.board
        moves = [x for x, item in enumerate(board) if item == 0]
        for x in range(expansion_size):
            temp = board
            temp[x] = self.turn_conversion[node.depth % 2]
            node.add_subnode(Node(board=temp, parent=node, depth=node.depth + 1))
        return node.subnodes

    def gen_layers(self,layers):
        curr_depth = self.depth
        while not self.depth - curr_depth >= layers:
            self.next_layer()

    def convert_board(self, b, c):
        for x, item in enumerate(b):
            b[x] = c[item]
        return b

    def update_root_node(self, new_root_node):
        self.root_node = new_root_node
        self.depth -= 1

































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


