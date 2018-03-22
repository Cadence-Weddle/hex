# Important Notice: Only call this file from root (Game Directory).
import random
import numpy as np
import AI.GameLogic.GameLogic as GameLogic
import AI.TreeSearch.MonteCarloTreeSearch as MonteCarloTreeSearch
from copy import deepcopy
import time
import threading
import keras

MCTS = MonteCarloTreeSearch.MonteCarloTreeSearch
NNBP = MonteCarloTreeSearch.Neural_Network_Batch_Processer
Game = GameLogic.Game

nn = keras.models.load_model("AI\\NeuralNetwork\\SavedModel.h5")
mcts = MCTS(Game(), nn)

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

def MakeMove(computetime, board, humanplayer,):
		board = np.array([x if x == 1 or x == 0 else -1 for x in board])
		mcts.root_node = mcts.top
		mcts.execute_history(gen_history(game.board))
		move = mcts.turn(computetime, convert_to_root=False)
		gamestate = mcts.Game.GameState
		mcts.game = Game()
		return {'moveloc' : str(move), 'gamestate': str(gamestate)}