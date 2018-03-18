import sys
sys.path.append("C:\\Users\\user\\Desktop\\Github\\hex.github.io\\Game\\AI\\")

import random
import numpy as np
import AI.GameLogic.GameLogic as GameLogic
import AI.TreeSearch.MonteCarloTreeSearch as MonteCarloTreeSearch
import AI.NeuralNetwork.NeuralNetwork as NeuralNetwork

MCTS = MonteCarloTreeSearch.MonteCarloTreeSearch
NN = NeuralNetwork.NeuralNetwork

def _MakeMove(computetime,board,humanplayer):
	return {'moveloc':str(np.random.choice([x for x in range(121)])),'gamestate':str(np.random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2]))}


def MakeMove(computetime, board, humanplayer,):
		Game = GameLogic.Game()
		Game.board = np.array([x if x == 1 or x == 0 else -1 for x in board])
		Game.NextPlayer = -1
		Game.InvertBoard()
		mcts = MCTS(Game, NN())
		move = mcts.turn(11)
		Game.MakeMove(move)
		return {'moveloc' : str(move), 'gamestate': str(Game.GameState)}