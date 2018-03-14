from GameTree import *
from copy import deepcopy as copy
import numpy as np

def UCT(*args): #MAGIck 
	return 0

def argmax(list):
	return sorted(list, key=lambda x: x.mean_action_value)[0]

def sum_nodes(list):
	return sum([lambda x:x.mean_action_value for x in list])

class Not_Proccessed:
	pass

class ArrayWrapper:
	"""
	Allows for the use of np.ndarray s as dictionary keys in Neural_Network_Batch_Proccesser
	"""
	def __init__(self, array):
		self.array = array
	def __hash__(self):
		return tuple(self.array.flatten()).__hash__()
	def __eq__(self, array):
		return array == self.array
	def unpack(self):
		return array

class Neural_Network_Batch_Processer:
	"""
	For storing and proccessing data in bulk.
	Also functions as a cache. It stores the evaluated boards and doesn't recompute them if a different node with the same board is requested. 
	"""
	
	def __init__(self, model, MaxCacheSize=10000):
		self.queue = []
		self.return_dict = {}
		self.model = model

	def run_batch(self):
		outs = self.model.foward_prop([x.game.board for x in self.queue])
		for x, i in enumerate(self.queue):
			self.return_dict[tuple(i.game.board.flatten())] = outs[x]

	def __getitem__(self, node):
		try:
			if self.return_dict[tuple(node.game.board.flatten())] is Not_Proccessed():
				if not node in self.queue:
					self.queue.append(node)
				self.run_batch()
		except KeyError:
			if not node in self.queue:
				self.queue.append(node)
			self.run_batch()
		return self.return_dict[tuple(node.game.board.flatten())]		

	def add_node(self, node):
		if not node in self.queue and not tuple(node.game.board.flatten()) in self.return_dict.keys():
			self.queue.append(node)
			#self.return_dict[tuple(node.game.board.flatten())] = Not_Proccessed()

	def add_list(self, list):
		for node in list:self.add_node(node)


class  MCTS_Node(Node):
	"""docstring for  MCTS_Node"""
	def __init__(self, game, parent, processer, get_moves="get_valid_moves", make_move="make_move"):
		super().__init__(game, parent, get_moves=get_moves, make_move=make_move)

		#Section Reinforcement in AlphaGo Zero Page 255, Nature Vol 550
		self.visit_count = 0        # N(s,a)
		self.total_action_value = 0 # W(s,a)
		self.mean_action_value = 0  # Q(s,a) || Acts as "score" it is what the MCTS considers. 

		self.score = 0 #Neural network based evaluation | Ignores subnodes. 
		self.processer = processer # "pointer" to the neural network batch processer. 
		self.expanded = False #Reached by MCTS search during the selection phase. 
		self.value = 0 #Value head of network evalutaion, different from score.
		self.prior_probability = 0 #Created during evaluation of node which happens when the parent node is expanded. 
		self.subnode_probs = {x : 0 for x in self.subnodes}
		self.evaluation_function = UCT


	@staticmethod
	def _compute_score(node, method, exploration_constant=1): # U(s,a)
		if type(node) != MCTS_Node:
				raise TypeError('MCTS_Node Score can only be computed for said type| Data:{data}'.format(dir(node)))
		return method(node, exploration_constant)

	def update_score(self):
		if not self.score:
			self.score = MCTS_Node._compute_score(self, self.evaluation_function)
			self.mean_action_value = self.score
			return
		self.mean_action_value = (sum(self.subnodes) + self.score) / (len(self.subnodes) + 1) #Probably need to change---Just averages the nn value with the values of the subnodes. 

	def set_nn_output(self, x):
		P, v = x
		self.value = v
		self.prior_probability = P
		self.update_score()
	
	def expand(self):
		valid_moves = getattr(self.game, self.get_moves)()	
		subnodes = []

		for move in valid_moves:
			temp = copy(self.game)
			getattr(temp, self.make_move)(move)
			subnodes.append(MCTS_Node(temp, self, self.processer, self.get_moves, self.make_move))
		self.processer.add_list(subnodes)

		for node in subnodes:
			node.set_nn_output(self.processer[node])
		self.subnodes = subnodes
		self.update_score()
		return subnodes
	def __str__(self):
		return "{type_self}, Parent : {parent}, Number of subnodes : {subnodes}, expanded : {expanded}".format(type_self=type(self), parent=type(self.parent),subnodes=len(self.subnodes)
		,expanded=self.expanded)


class MonteCarloTreeSearch(Tree):
	def __init__(self, game, model, **kwargs):
		self.game = game
		self.batch_processer = Neural_Network_Batch_Processer(model)
		super().__init__(game, root_node=MCTS_Node(game, None, self.batch_processer, "GetValidMoves", "MakeMove"))#kwargs.get("get_moves", "get_valid_moves"), make_move=kwargs.get("make_move", "make_move")))

	def select(self):
		curr_node = self.root_node
		while curr_node.expanded:
			curr_node = argmax(curr_node.subnodes)
			curr_node.visit_count += 1
			print(curr_node)
		return curr_node	

	def expand_and_eval(self, node):
		node.expanded = True
		node.expand()
		return node

	def back_prop(self, node):
		while node.parent:
			node.update_score()
			node = node.parent

	def turn(self, iterations):
		for i in range(iterations):
			self.back_prop(self.expand_and_eval(self.select()))
		return argmax(self.root_node.subnodes)