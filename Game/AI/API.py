# Important Notice: Only call this file from root (Game Directory).
import random
import numpy as np
import AI.GameLogic.GameLogic as GameLogic
import AI.TreeSearch.MonteCarloTreeSearch as MonteCarloTreeSearch
import AI.NeuralNetwork.NeuralNetwork as NN
from copy import deepcopy
import time
import threading
import keras

NN = NN.NeuralNetwork
MCTS = MonteCarloTreeSearch.MonteCarloTreeSearch
NNBP = MonteCarloTreeSearch.Neural_Network_Batch_Processer
Game = GameLogic.Game
def open():
	nn = NN.NNCreater(keras.models.load_model("AI\\NeuralNetwork\\SavedModel.h5"))
	return nn

nn = open()

def _MakeMove(computetime,board,humanplayer):
	return {'moveloc':str(np.random.choice([x for x in range(121)])),'gamestate':str(np.random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2]))}

def gen_history(board):
        """
        #Returns a possible history of moves that could have led to that state. 
        """
        board = np.array(board)
        p1 = np.where(board == 1)[0]
        p2 = np.where(board == 2)[0]
        lesser = min(len(p1),len(p2))
        return np.stack((p2[:lesser],p1[:lesser])).flatten('F')

def MakeMove(computetime, board, humanplayer=None,):
		mcts = MCTS(Game(), nn)
		board = np.array([x if x == 1 or x == 0 else -1 for x in board])
		mcts.execute_history(gen_history(board))
		move = mcts.turn(computetime, convert_to_root=False)
		gamestate = mcts.game.GameState
		return {'moveloc' : str(move), 'gamestate': str(gamestate)}

def _MakeMove_(computetime, board, humanplayer=None):
	game = Game()
	game.board = [x if x == 1 else -1 for x in board]
	game.NextPlayer = -1
	game.InvertBoard()
	mcts = MCTS(game, NN())
	return {'moveloc' : mcts.turn(10), 'gamestate' : str(mcts.game.GameState)}