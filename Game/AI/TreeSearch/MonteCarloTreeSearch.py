from AI.TreeSearch.GameTree import *
from copy import deepcopy as copy
import numpy as np
import random
import time

def UCT(node, exploration_constant): #Magick? Please fix 
	return exploration_constant	* node.prior_probability * (np.sqrt(node.visit_count + 1) / (node.visit_count + 1))


def argmax(list):
	return sorted(list, key=lambda x: x.mean_action_value)[0]

def sum_nodes(list):
	return sum([(lambda x:x.mean_action_value)(x) for x in list])

def hash(ndarray):
	return tuple(ndarray.flatten()).__hash__()

class Not_Proccessed:
	pass


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
			self.return_dict[hash(i.game.board)] = outs[x]

	def __getitem__(self, node):
		try:
			if self.return_dict[hash(node.game.board)] is Not_Proccessed():
				if not node in self.queue:
					self.queue.append(node)
				self.run_batch()
		except KeyError:
			if not node in self.queue:
				self.queue.append(node)
			self.run_batch()
		return self.return_dict[hash(node.game.board)]		

	def add_node(self, node):
		if not node in self.queue and not hash(node.game.board) in self.return_dict.keys():
			self.queue.append(node)
			#self.return_dict[hash(node.game.board)] = Not_Proccessed()

	def add_list(self, list):
		for node in list:self.add_node(node)


class  MCTS_Node(Node):
	"""docstring for  MCTS_Node"""
	def __init__(self, game, parent, processer, move, prior_probability=0, get_moves="get_valid_moves", make_move="make_move"):
		super().__init__(game, parent, get_moves=get_moves, make_move=make_move)
		self.visit_count = 0        # N(s,a)
		self.mean_action_value = 0  # Q(s,a) || Acts as "score" it is what the MCTS considers. 

		self.score = 0 #Neural network based evaluation | Ignores subnodes. 
		self.processer = processer # "pointer" to the neural network batch processer. 
		self.expanded = False #Reached by MCTS search during the selection phase. 
		self.value = 0 #Value head of network evalutaion, different from score.
		self.prior_probability = prior_probability #Taken from the Parent node
		self.evaluation_function = UCT #Magic
		self.move = move #move required to take the game from the parent node's state to the current state.

	@staticmethod
	def _compute_score(node, method, exploration_constant=1): # U(s,a)
		if type(node) != MCTS_Node:
				raise TypeError('MCTS_Node Score can only be computed for said type| Data:{data}'.format(dir(node)))
		return method(node, exploration_constant)

	def update_score(self):
		self.score = MCTS_Node._compute_score(self, self.evaluation_function)
		self.mean_action_value = (sum_nodes(self.subnodes) + self.value) / (len(self.subnodes) + 1)
		self.score += self.mean_action_value #Probably need to change---Just averages the nn value with the values of the subnodes. 
		if self.game.GameState != 0:
			self.reward = -1

	def set_nn_output(self, x):
		P, v = x
		self.value = v
		self.p = P
		self.update_score()
	
	def expand(self):
		valid_moves = getattr(self.game, self.get_moves)()	
		subnodes = []
		r_probs = self.p.reshape([121])
		for move, p in zip(valid_moves, r_probs):
			temp = copy(self.game)
			getattr(temp, self.make_move)(move)
			subnodes.append(MCTS_Node(temp, self, self.processer, move, p, self.get_moves, self.make_move))
		self.processer.add_list(subnodes)

		for node in subnodes:
			node.set_nn_output(self.processer[node])
		self.subnodes = subnodes
		self.update_score()

		return subnodes

	def dump(self):
		return (self.game.board.reshape([11,11,1]), self.reward)

	def __str__(self):
		return "{type_self}, Parent : {parent}, Number of subnodes : {subnodes}, expanded : {expanded}, move : {move}".format(type_self=type(self), parent=type(self.parent),subnodes=len(self.subnodes)
		,expanded=self.expanded, move=self.move)
	def __repr__(self):
		return self.__str__()

	def __getitem__(self, move):
		for subnode in self.subnodes:
			if subnode.move == move:
				return subnode
		return None

class MonteCarloTreeSearch(Tree):
	def __init__(self, game, model=None, processer=None,  **kwargs):
		self.game = game
		self.batch_processer = processer if processer else Neural_Network_Batch_Processer(model)

		super().__init__(game, root_node=kwargs.get("rn", MCTS_Node(game, None, self.batch_processer, 0, get_moves="GetValidMoves", make_move="MakeMove")))#kwargs.get("get_moves", "get_valid_moves"), make_move=kwargs.get("make_move", "make_move")))
		self.top = self.root_node

		self.batch_processer.add_node(self.root_node)
		self.root_node.set_nn_output(self.batch_processer[self.root_node])

	def execute_history(self, history):
		game = self.game
		curr_node = self.root_node
		for move in history:
			game.MakeMove(move)
			if not curr_node.expanded:
				curr_node.expand()
			curr_node = curr_node[move]
		self.root_node = curr_node

	def select(self):
		curr_node = self.root_node
		while curr_node.expanded:
			if curr_node.game.GameState != 0:
				break
			curr_node = argmax([node for node in curr_node.subnodes if not node.game.GameState])
			curr_node.visit_count += 1
		return curr_node	

	def expand_and_eval(self, node):
		node.expanded = True
		node.expand()
		return node

	def back_prop(self, node):
		while node.parent:
			node.update_score()
			node = node.parent

	def turn(self, ComputeTime):
		start = time.time()
		i = 0
		while time.time() - start < ComputeTime / 1000:
			if not i:
				i +=1
			self.back_prop(self.expand_and_eval(self.select()))

		node = argmax(self.root_node.subnodes)
		move = node.move
		self.root_node = node
		self.root_node.convert_to_root()
		return move

	def train(self, gamma):
		model = self.batch_processer.model
		history = self.game.history
		training_data = []
		curr_node = self.top
		for move in history:
			curr_node = curr_node[move]
		history = history[::-1]
		i = 1
		curr_node.reward = curr_node.game.NextPlayer
		while curr_node.parent:
			training_data.append(curr_node.dump)
			curr_node.parent.reward = curr_node.parent[history[i]].reward * gamma
			i += 1
			curr_node = curr_node.parent 

		pData = [x[1] for x in training_data]
		vData = [x[2] for x in training_data]
		inData = [x[0] for x in training_data]
		return pData, inData, vData
