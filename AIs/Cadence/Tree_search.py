
from Heuristic import score
import sys
import time

def max_node(*args):                        
    current_max = args[0]                   
    for node in args[1:]:                   
        if node.score > current_max.score:  
            current_max = node              
    return current_max                      
                                            
                                            
def min_node(*args):                        
    curr_min = args[0]
    for node in args[1:]:
        if node.score < curr_min:
            curr_min = node
    return curr_min

def iter_flatten(iterable):
  it = iter(iterable)
  for e in it:
    if isinstance(e, (list, tuple)):
      for f in iter_flatten(e):
        yield f
    else:
      yield e

class Node():
    def __init__(self, board, parent, depth,heuristic, score=None):
        self.parent = parent
        self.board = board
        self.subnodes = []
        self.score = score
        self.depth = depth
	self.heuristic = heuristic
    def sort_subnodes(self,func=score):
        return sorted(self.subnodes, key=func)


    def add_subnode(self,node, sort=True):
        self.subnodes.append(node)
        if sort:
            self.subnodes = self.sort_subnodes()

   def expand(self, get_valid_moves, make_move, sort=True):
	board = self.board
	moves = get_valid_moves(board)
	for move in get_valid_moves:
		self.subnodes.append(make_move(board, move)
	self.sort_subnodes()
	return self.subnodes
    def __getitem__(self, *key):
        return "NOT IMPLEMENTED"


class Tree():

    def __init__(self, board, player, other_player, depth=0):
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

'''
    def alpha_beta_tree_search(self, alpha, beta, node, depth, maximizing_player, max_depth=4):
        if depth == max_depth:
            node.score = score(node.board)
            return node
        if not node.subnodes:
            self.expand_node(node)
        if maximizing_player:
            value = Node(None, None, None, score=-3267) #Negitive infinity
            for subnode in node.subnodes:
                max_node = self.alpha_beta_tree_search(alpha, beta, subnode, depth + 1, maximizing_player=False, max_depth=max_depth)
                value = max_node(value, max_node)
                alpha = max_node(value, alpha)
                if beta <= alpha:
                    break
            return value
        else:
            value = Node(None, None, None, score=999999999999999999999)  # positive infinity
            for subnode in node.subnodes:
                min_node = self.alpha_beta_tree_search(alpha, beta, subnode, depth + 1, maximizing_player=True, max_depth=max_depth)
                value = min_node(value, min_node)
                beta = min_node(value, beta)
                if beta <= alpha:
                    break
            return value
    def alpha_beta_predict(self, depth):
        node = self.alpha_beta_tree_search(Node(None, None, None, score=-999999999999999999999), Node(None,None,None, score=999999999999999999999), self.root_node,depth = 0, maximizing_player=self.player_is_first, max_depth=depth)
        curr_node = node
        parent_node = node.parent
        while True:
            try:
                curr_node = parent_node
                parent_node = curr_node.parent
            except:
                break
        return curr_node, node
'''
