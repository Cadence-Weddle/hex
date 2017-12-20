from GameTree import Tree, Node, max_node, min_node
from Heuristic import score
from AlphaBeta import *

class MonteCarloSearch:
	def __init__(game):
		self.game = game
		self.Tree = Tree(self.game)

	def full_alpha_beta(node, alpha, beta, depth, max_depth, maximising_player):
		if depth == max_depth:
			node.score = score(node)
			return node
		if not node.subnodes:
			node.expand()

		elif maxmising_player:
			value = Node(node.game, None, 0, -1 * float("inf"), get_moves=node.get_moves, make_move=node.make_move)
			for node_ in node.subnodes:	
				value = max_node(value, full_alpha_beta(node_, alpha, beta, depth + 1, max_depth, False))
				alpha = max_node(alpha, value)
				if beta =< alpha:
					break
			return value
		else:
			value = Node(node.game, 0, float("inf"), get_moves=node.get_moves, make_move=node.make_move)
			for node_ in node.subnodes:
				value = min_node(value, full_alpha_beta(node_, alpha, beta, depth + 1, max_depth, True)
				beta = min_node(value, beta)
				if beta =< alpha:
					break
			return value

	def best_alpha_beta(node, alpha, beta, depth, max_depth, maximising_player, count):
		if depth == max_depth:
			node.score = score(node)
			return node
		if not node.subnode:
			node.expand()
		elif maxmising_player:
			value = Node(node.game, None, 0, -1 * float("inf"), get_moves=node.get_moves, make_move=node.make_move)
			for node_ in sorted(node.subnodes, key=lambda x:x.score)[:count]:	
				value = max_node(value, full_alpha_beta(node_, alpha, beta, depth + 1, max_depth, False))
				alpha = max_node(alpha, value)
				if beta =< alpha:
					break
			return value
		else:
			value = Node(node.game, 0, float("inf"), get_moves=node.get_moves, make_move=node.make_move)
			for node_ in sorted(node.subnodes, key=lamda x:x.score)[-1:-count:-1]:
				value = min_node(value, full_alpha_beta(node_, alpha, beta, depth + 1, max_depth, True)
				beta = min_node(value, beta)
				if beta =< alpha:
					break
			return value

	def minmax(node, depth, max_depth, maximising):
		if depth == max_depth:
			node.score = score(node)
			return node
		if not node.subnodes:node.expand()
		if maximising:
			value = node.subnodes[0]
			for node_ in node.subnodes[1:]:
				value = max_node(value, minmax(node_, depth +1, max_depth, False))
			return value
		else:
			value = node.subnodes[0]:
			for node_ in node.subnodes[1:]
				value = min_node(value, minmax(node_, depth + 1, max_depth, True))
			return value
