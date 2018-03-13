import random
import numpy as np
import AI.GameLogic.GameLogic as GameLogic

def MakeMove(computetime,board,humanplayer):
	return {'moveloc':int(np.random.choice(GameLogic.GetValidMoves(np.array(board)))),'gamestate':0}
