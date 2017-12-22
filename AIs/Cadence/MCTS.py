from GameTree import Tree, Node, max_node, min_node
from Heuristic import score

class MonteCarloSearch:
	def __init__(game):
		self.game = game
		self.Tree = Tree(self.game)

	def full_MCTS(Node,C=2,**kwargs):
		def UCB1(node):
			if node.depth == 0:
				# If root node. May be implemented using depth
				(node.score/node.visits)
			else:
				#This matah will break, it will be fixed
				return (node.score/node.visits)+C*(math.sqrt(math.log(node.parent.visits/node.visits)))

		def Rollout(node):

		def Propogate(node,Heuristic=Rollout):
			#Can either use Rollout or Value network
			for child in node.subnodes:
				child.value = UCB1(node)
			#This should return a list in the event that some unvisited nodes have equal UCB1 vaulues, which is quite common in MCTS
			Highest_UCB_Node = random.choice(max_node(node.subnodes))
			return Heuristic(Highest_UCB_Node)
			
		def Backprop(node,value):




'''
	def full_alpha_beta(node,):
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
'''
