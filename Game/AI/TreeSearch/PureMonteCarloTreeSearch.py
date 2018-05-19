from AI.TreeSearch.GameTree import *
from copy import deepcopy as copy
import numpy as np
import random
import time

def div(a, b):
	if b == 0:
		return 1
	else:
		return a/b
def product(list):
	i = 1
	for k in list:
		i *= list[k]
	return i

def sum_nodes(list, attr='wins'):
	return sum([(lambda x:getattr(x, attr))(x) for x in list])

def argmax(list, all=False):
	return sorted(list, key=lambda x: div(x.wins, x.visits))[0]

def argmax_(list, all=False):
	return sorted(list)[0]

def ProportionalRandom(list):
	s = product([x.visits for x in list])
	print(s)
	o = []
	for item in list:
		for k in range(argmax_([1, int(item.wins * (s / item.visits))])):
			o.append(item)

	return random.choice(o)



def normilize(array):
	if sum(array) == 0:
		return array
	else:
		return array / np.sum(array)

def policy(node):
		game = copy(node.game)
		player = game.NextPlayer
		value = 0
		c = len(game.history)
		while not game.GameState:
			game.MakeMove(random.choice(game.GetValidMoves()))
		return game.GameState  * (1 if game.NextPlayer == player else -1)


class  MCTS_Node(Node):
	"""docstring for  MCTS_Node"""
	def __init__(self, game, parent,  move, get_moves="get_valid_moves", make_move="make_move"):
		super().__init__(game, parent, get_moves=get_moves, make_move=make_move)
		self.visits = 1
		self.wins = 0  
		self.expanded = False #Reached by MCTS search during the selection phase. 
		self.move = move #move required to take the game from the parent node's state to the current state.
		self.score = self.wins / self.visits

	def UpdateScore(self):
		if not self.expanded:
			self.expand()
		self.wins = sum_nodes(self.subnodes)
		self.visits = sum_nodes(self.subnodes, "visits")
		self.score = self.wins / self.visits


	def expand(self):
		if not self.game.GameState or not self.expanded:
			self.expanded = True
			valid_moves = getattr(self.game, self.get_moves)()
			subnodes = []
			for move in valid_moves:
				temp = copy(self.game)
				getattr(temp, self.make_move)(move)
				subnodes.append(MCTS_Node(temp, self,move, self.get_moves, self.make_move))
			
			self.subnodes = subnodes
			self.UpdateScore()
			self.play()
			return subnodes
		elif self.game.GameState:
			self.wins = self.game.GameState
			self.visits = 1


	def play(self):
		choice = random.choice(self.subnodes)
		if choice.game.GameState:
			result = choice.game.GameState	
		else:
			choice.visits += 1
			result = policy(choice)
		if result == 1:
			choice.wins += 1
		else:
			return

	def dump(self):
		pArray= [] #Coverted into 'correct' policy head output
		subnode_choices = [subnode.move for subnode in self.subnodes]
		for i in range(121):
			try:
				if i in subnode_choices:
					pArray.append(self.subnodes[subnode_choices.index(i)].wins)
				else:
					pArray.append(0)
			except:
				pArray.append(0)
		return (self.game.board.reshape([11,11,1]), normilize(np.array(pArray)), self.reward)


	def __str__(self):
		return "{type_self}, Parent : {parent}, Number of subnodes : {subnodes}, expanded : {expanded}, move : {move}".format(type_self=type(self), parent=type(self.parent),subnodes=len(self.subnodes)
		,expanded=self.expanded, move=self.move)
	
	def __repr__(self):
		return self.__str__()

	def __getitem__(self, move):
		for subnode in self.subnodes:
			if subnode.move == move:
				return subnode
		raise Exception("Couldn't find move {} in valid_moves {}".format(move, self.game.GetValidMoves()))


class MonteCarloTreeSearch(Tree):
	def __init__(self, game,  **kwargs):
		self.game = game
		super().__init__(copy(game), root_node=kwargs.get("rn", MCTS_Node(game, None, None, get_moves="GetValidMoves", make_move="MakeMove")))
		self.top = self.root_node


	def execute_history(self, history):
		game = self.game
		curr_node = self.root_node
		for move in history:
			print(move)
			game.MakeMove(move)
			curr_node.expand()
			curr_node = curr_node[move]
			print("done")
		self.root_node = curr_node
		self.root_node.convert_to_root()


	def select(self):
		curr_node = self.root_node
		while curr_node.expanded:
			if curr_node.game.GameState != 0:
				break
			if curr_node.subnodes == []:
				raise Exception("Something Bad Happened")
			curr_node = random.choice([node for node in curr_node.subnodes if not node.game.GameState])
			curr_node.visits += 1
		return curr_node	

	def expand_and_eval(self, node):
		node.expanded = True
		node.expand()
		return node

	def back_prop(self, node):
		while node.parent:
			node.UpdateScore()
			node = node.parent

	def turn(self, ComputeTime, convert_to_root=True):
		start = time.time()
		while time.time() - start < ComputeTime / 1000:
			self.back_prop(self.expand_and_eval(self.select()))
		node = argmax(self.root_node.subnodes)
		move = node.move
		if convert_to_root:
			self.root_node = node
			self.root_node.convert_to_root()
		self.game.MakeMove(move)
		return move
