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
	def __init__(self, game, parent, get_moves="get_valid_moves", make_move="make_move"):
		"""
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
			sort_subnodes(func) := Returns a list of subnodes which has been sorted according terminal_node func
			expand() := Generates all nodes which can be reached by making 1 move and assigns that list to self.subnodes
			convert_to_root(moves) := Converts this node to a root node. Moves is the amount of moves it takes to do this (defaults to 1)

		"""
		self.parent = parent
		self.game = game
		self.subnodes = []
		self.score = 0
		self.make_move = make_move
		self.get_moves = get_moves


		#Checking inputs
		try:		
			game = self.game
			assert type(parent) in (None, type(self))
			getattr(game, self.get_moves)
			getattr(game, self.make_move)
		except:
			print("An error occured while type Checking; parent : {parent}, type(self) : {type_self}".format(parent=parent, type_self=type(self)))

	def add_subnode(self,node):
		self.subnodes.append(node)

	def expand_node(self):
		game = self.game
		moves = getattr(game, self.get_moves)()
		for move in moves:
			temp_game = game
			getattr(temp_, self.make_move)(move)
			self.add_subnode(Node(temp_game, self, self.depth + 1, get_moves=self.get_moves, make_move=self.make_move))
		return self.subnodes

	def convert_to_root(self):
		self.parent = None

	def __str__(self):
		return "{type_self}, Parent : {parent}, Number of subnodes : {subnodes}}".format(type_self=type(self), parent=type(self.parent),subnodes=len(self.subnodes))


class Tree:
	def __init__(self, game, root_node=None, **kwargs):
		self.game = game
		if not root_node:
			self.root_node = Node(game, None, 0)
		else:
			self.root_node = root_node
	def update_root_node(self, new_root_node):
		self.root_node = new_root_node
		self.root_node.convert_to_root()
	




#self.root_node = kwargs.get('root_node', Node(game, None, 0, get_moves=kwargs.get("get_valid_moves", "get_valid_moves"), make_move=kwargs.get("make_move", "make_move")))
