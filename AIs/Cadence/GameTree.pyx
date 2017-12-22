

def iter_flatten(iterable):
	it = iter(iterable)
	for e in it:
		if isinstance(e, (list, tuple)):
			for f in iter_flatten(e):
				yield f
		else:
			yield e

def max_node(*args):
	curr_max = args[0]
	for node in args[1:]:
		if node.score > curr_max.score:
			curr_max = node
	return curr_max

def min_node(*args):
	curr_min = args[0]
	for node in args[1:]:
		if node.score < curr_min.score:curr_min = node
	return curr_min

class Node:
	def __init__(self, game, parent, int depth, float score=0, get_moves="get_valid_moves", make_move="make_move"):
		'''
	Args:
		self := Class instance
		game := Self explanatory
		parent := Parent node, None if this node is the root node in the tree
		depth := The depth of the node
		score := The value of this node: In the case of MCTS the total value of the state
		get_moves := String of the method name which returns a list of valid moves. This method is an attribute of game
		make_move := String of the method name which returns a game which has had a move made. This method is an attribute of game

	Methods:
		__init__ := default constructor
		sort_subnodes(func) := Returns a list of subnodes which has been sorted according to func
		expand() := Generates all nodes which can be reached by making 1 move and assigns that list to self.subnodes
		convert_to_root(moves) := Converts this node to a root node. Moves is the amount of moves it takes to do this (defaults to 1)

		'''
	self.parent = parent
	self.game = game
	self.subnodes = []
	self.score = score
	self.depth = depth
	self.make_move = make_move
	self.get_moves = get_moves
	self.visit_count = 1

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
			self.add_subnode(Node(getattr(game, self.make_move)(move), self, self.depth + 1, get_moves=self.get_moves, make_move=self.make_move), sort=False)
		return self.subnodes

	def convert_to_root(self, moves=1):
		self.parent = None
		self.update_depth(moves)

	def update_depth(self, thing):
		self.depth -= thing
		if not self.subnodes:
			for node in self.subnodes:
				node.update_depth(thing)

class Tree:

	def __init__(self, game, **kwargs):
		self.game = game
		self.root_node = Node(game, None, 0, get_moves=kwargs.get("get_valid_moves", "get_valid_moves"), make_move=kwargs.get("make_move", "make_move"))
		self.terminal_nodes = self.root_node.subnodes


	def next_layer(self):
		nodes = []
		for node in self.terminal_nodes:
			nodes.append(self.expand_node(node, add_to_terminal_nodes=False))
		nodes = [i for i in iter_flatten(nodes)]
		self.terminal_nodes = nodes
		self.depth += 1
		return list(set(nodes))

	def expand_node(self, node, add_to_terminal_nodes=True):
		nodes = node.expand()
		if add_to_terminal_nodes:	
			index = [i for i, x in enumerate(self.terminal_nodes) if x == node][0]
			self.terminal_nodes.pop(index)
			self.terminal_nodes = [i for i in iter_flatten(self.terminal_nodes.append(nodes))]
		return nodes

	def convert_board(self, b, c):
		for x, item in enumerate(b):
			b[x] = c[item]
		return b

	def update_root_node(self, new_root_node):
		self.root_node = new_root_node
		self.root_node.update_depth(1)
		self.depth -= 1








'''
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
'''
