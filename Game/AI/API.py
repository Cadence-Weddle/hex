# Important Notice: Only call this file from root (Game Directory).
import random
import numpy as np
import AI.GameLogic.GameLogic as GameLogic
import AI.TreeSearch.MonteCarloTreeSearch as MonteCarloTreeSearch
import AI.NeuralNetwork.NeuralNetwork as NeuralNetwork
from copy import deepcopy
import time
import threading

MCTS = MonteCarloTreeSearch.MonteCarloTreeSearch
NN = NeuralNetwork.NeuralNetwork
NNBP = MonteCarloTreeSearch.Neural_Network_Batch_Processer
Game = GameLogic.Game


def _MakeMove(computetime,board,humanplayer):
	return {'moveloc':str(np.random.choice([x for x in range(121)])),'gamestate':str(np.random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2]))}

def MakeMove(computetime, board, humanplayer,):
		Game = GameLogic.Game()
		Game.board = np.array([x if x == 1 or x == 0 else -1 for x in board])
		Game.NextPlayer = -1
		Game.InvertBoard()
		mcts = MCTS(Game, NN())
		move = mcts.turn(computetime)
		return {'moveloc' : str(move), 'gamestate': str(Game.GameState)}

class MCTS_Manager(threading.Thread):
	def __init__(self):
		self.game = Game()
		self.nn = NN()
		self.NNBP = NNBP(self.nn)
		self.mcts = MCTS(self.game, processer=self.NNBP)

if __name__ == "__main__":
	game = Game()
	nn = NN()
	main(MCTS(game, nn))