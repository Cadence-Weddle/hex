import random
<<<<<<< HEAD
import numpy as np

def MakeMove(computetime,board,humanplayer):
	return {'moveloc':random.choice(np.argwhere(np.array(board)==0)[0]),'gamestate':0}
=======

def MakeMove(computetime,board,humanplayer):
    return {'moveloc':random.choice([x for x in range(121)]),'gamestate':0}


>>>>>>> 110e644cf50c230719c4f10080818f5bb4027709
