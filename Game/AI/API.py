import random
import numpy as np
import AI.GameLogic.GameLogic

def MakeMove(computetime,board,humanplayer):
	return {'moveloc':random.choice(GameLogic.GetValidMoves(np.array(board))),'gamestate':0}
