import sys
sys.path.append("C:\\Users\\user\\Desktop\\Github\\hex.github.io\\Game\\AI\\")

import random
import numpy as np
import AI.GameLogic.GameLogic as GameLogic
from TreeSeach.MonteCarloTreeSearch import MonteCarloTreeSearch as MCTS
from NeuralNetwork.NeuralNetwork import NeuralNetwork as NN
def _MakeMove(computetime,board,humanplayer):
	return {'moveloc':str(np.random.choice([x for x in range(121)])),'gamestate':str(np.random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2]))}


def MakeMove(computetime, board, humanplayer,):
		Game = GameLogic.Game()
		Game.board = [x if x == 1 or x == 0 else -1 for x in board]
		Game.NextPlayer = -1
		Game.InvertBoard()
		mcts = MCTS(Game, NN())
		return {'moveloc' : MCTS.turn(10), 'gamestate': str(np.random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2]))}