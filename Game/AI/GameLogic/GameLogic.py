import numpy as np

def MakeMove(board,location,player):
	"""
	DOES NOT RETURN COPY OF THE BOARD. MODIFIES NP.ARRAY OBJECT ITSELF
	Puts a player's value into the board
	Board must be an np array
	location and player must be integers

	"""
	if board[location] == 0 and ((player==1) or (player==2)):
		return np.put(board,location,player)
	else:
		raise ValueError('Invalid Input')

def GetValidMoves(board):
	"""
	Get all valid moves for a given board.
	"""
	return np.where(board == 0)

def SwitchPlayer(player,schema=1):
	"""
	Returns the other player
	schema 0: players are 0 and 1
	schema 1: players are 1 and 2
	"""
	if schema:
		return not(player)
	else:
		return not(player-1)+1