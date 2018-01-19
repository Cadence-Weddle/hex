from GameTree import Tree, Node, max_node, min_node
from Heuristic import score
import tensorflow as tf
import numpy as np
from scores import *
from copy import deepcopy as copy



def policy_wrapper(NeuralNetwork, device="/cpu:0"):
	def func(game):
		board = game.board
		with tf.Session() as sess:
			with tf.device(device):
				return NeuralNetwork.predict(board)
	return func

class Not_Proccessed:
	def __init__():


def Neural_Network_Batch_Processer:
	def __init__(model, max_batch_size=121):
		self.queue = []
		self.max_batch_size = max_batch_size
		self.return_dict = {x.game.board : Not_Proccessed() for x in self.queue}
	def run_batch(self):
		outs = self.model.predict_batch([x.game.board for x in self.queue])
		for x, i in enumerate(self.queue):
			self.return_dict[i.game.board] = outs[x]

	def __getitem__(self, node):
		if self.return_dict[node.game.board] is Not_Proccessed():
			self.run_batch()
		return self.return_dict[node.game.board]

	def __setitem__(self, *args):
		raise NotImplemented

	def add_node(self, node):
		if not node in self.queue and not node.game.board in self.return_dict.keys():
			self.queue.append(node)

	def add_list(self, list):
		for node in list:self.add_node(node)

Neural_Network_Batch_Processer_Instance = Neural_Network_Batch_Processer()




class  MCTS_Node(Node):
	"""docstring for  MCTS_Node"""
	def __init__(self, game, parent, processer, get_moves="get_valid_moves", make_move="make_move"):
		Node.__init__(game, parent, get_moves=get_moves, make_move=make_move)

		#Section Reinforcement in AlphaGo Zero Page 255, Nature Vol 550
		self.visit_count = 0        # N(s,a)
		self.total_action_value = 0 # W(s,a)
		self.mean_action value = 0  # Q(s,a)
		
		if self.parent is None: # Root node must be intialized 100% probablity
			self.prior_probability = 1
		else:	
			self.prior_probability = self.parent.subnode_probs[self.game] # P(s,a)

		self.processer = processer
		self.expanded = False
		self.score = 0
		self.value = 0 #Value head of network evalutaion, different from score.
		self.subnode_probs = {x : 0 for x in self.subnodes}


	@staticmethod
	def _compute_score(node, method=PUCT, exploration_constant=1): # U(s,a)
		if type(node) != MCTS_Node:
				raise TypeError('MCTS Node Score can only be computed for said type')
		
		return method(node,exploration_constant)

	def update_score(self):
		self.score = _compute_score(self)
		
	
	def expand():
		valid_moves = getattr(self.game, self.get_valid_moves)()
		subnodes = []
		for move in valid_moves:
			subnodes.append(MCTS_Node())



class MonteCarloSearch(Tree):
	def __init__(game, model, **kwargs):
		Tree.__init__(game, root_node=MCTS_Node(game, None, processer=self.batch_processer, get_moves=kwargs.get("get_valid_moves"), make_move=kwargs.get("make_move")))
		self.game = game
		self.policy = policy_wrapper(policy)
		self.batch_processer = Neural_Network_Batch_Processer(model)



	def back_prop(node, win):
		parent = node.parent
		node.update_score()
		while not parent is None:
			parent.update_score()

