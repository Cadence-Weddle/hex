import numpy as np
from copy import deepcopy as copy

class Game():
	def __init__(self):
		self.board = np.zeros([121,1])
		self.GameState = 0
		self.NextPlayer = 1
		self.NextMoveBoard = np.zeros([121,1]) #Helps with NN proccessing. This way "self.board" can be inverted without damaging the "MakeMove" and "GetValidMoves" functions, which are needed for the MTCS

	def MakeMove(self, location, player=None):
		player = player if player else self.NextPlayer
		MakeMove(self.NextMoveBoard, location, player, PlayerSchema={"player1" : 1, "player2" : -1})
		self.GameState = GetGameState(self.NextMoveBoard, PlayerSchema={"Player1" : 1, "Player2" : -1})
		self.NextPlayer = SwitchPlayer(self.NextPlayer)
		self.board = self.NextMoveBoard
		if self.NextPlayer == -1:
			self.InvertBoard()


	def GetValidMoves(self):
		board = self.NextMoveBoard
		return GetValidMoves(board)	

	def GetGameState(self):
		return self.GameState

	def InvertBoard(self):
		temp = copy(self.NextMoveBoard)
		for i, x in enumerate(temp):
			temp[i] = SwitchPlayer(x, schema=0)
		self.board = temp
	
	def __str__(self):
		return "[Game] Board : {board}, NextMoveBoard : {NextMoveBoard}, GameState : {GameState}, NextPlayer : {NextPlayer}".format(board=self.board, NextMoveBoard=self.NextMoveBoard, GameState=self.GameState, NextPlayer=self.NextPlayer)


def MakeMove(board,location,player, PlayerSchema={"player1" : 1, "player2" : 2}):
		"""
		DOES NOT RETURN COPY OF THE BOARD. MODIFIES NP.ARRAY OBJECT ITSELF
		Puts a player's value into the board
		Board must be an np array
		location and player must be integers

	"""
		if board[location][0] == 0 and (player in [PlayerSchema["player1"], PlayerSchema["player2"]]):
			np.put(board,location,player)
		else:
			raise ValueError('Invalid Input')
	
def GetValidMoves(board):
		"""
		Get all valid moves for a given board.
		"""
		temp = copy(board)
		return [x for x, i in enumerate(temp) if i == 0]

def SwitchPlayer(player,schema=1):
		"""
		Returns the other player
		schema 0: players are -1 and 1
		schema 1: players are 1 and 2

		"""
		if player == 0:
			return 0
		elif not schema:
			return -1 if player==1 else 1
		else:
			return 1 if player==2 else 2


def GetGameState(board, PlayerSchema={"Player1" : 1, "Player2" : 2}):
		return 0

