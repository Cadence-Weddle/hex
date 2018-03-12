import random
import numpy as np

def MakeMove(computetime,board,humanplayer):

	return {'moveloc':int(random.choice(np.argwhere(np.array(board)==0))[0]),'gamestate':0}
