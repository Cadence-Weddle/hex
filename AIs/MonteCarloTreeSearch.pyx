from GameTree import Tree, Node, max_node, min_node
from Heuristic import score
from AlphaBeta import *
import tensorflow as tf
import numpy as np

def policy_wrapper(NeuralNetwork, device="/cpu:0"):
	def func(game):
		board = game.board
		with tf.Session() as sess:
			with tf.device(device):
				return NeuralNetwork.predict(board)
	return func




class  MCTS_Node(Node):
	"""docstring for  MCTS_Node"""
	def __init__(self, game, parent, value, score=0, get_moves="get_valid_moves", make_move="make_move"):
		Node.__init__(game, parent, get_moves=get_moves, make_move=make_move)

		#Section Reinforcement in AlphaGo Zero Page 255, Nature Vol 550
		self.visits = 0 # N(s,a)
		self.expanded = False
		self.score = 0
		self.move_prob = 0 #P(s,a)
		self.value = value #Value head of network evalutaion, different from score.
		self.sim_subnodes = []

	@staticmethod
	def _compute_score(node):
		if type(node) != MCTS_Node:
				raise TypeError('MCTS Node Score can only be computed for said type')
		return ((np.mean([node.score for node in self.sim_subnodes]) + self.value) / (1 + self.visits)) #As per original alphago paper. 

	def update_score(self):
		self.score = _compute_score(self)
		
	

	def value():
		return # something


class MonteCarloSearch(Tree):
	def __init__(game, policy, **kwargs):
		Tree.__init__(game, root_node=MCTS_Node(game, None, 0, get_moves=kwargs.get("get_valid_moves"), make_move=kwargs.get("make_move")))
		self.game = game
		self.policy = policy_wrapper(policy)


	def back_prop(node, win):
		parent = node.parent
		node.update_score()
		while not parent is None:
			parent.update_score()

