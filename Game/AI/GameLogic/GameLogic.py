import numpy as np
from copy import deepcopy as copy

class Game():
<<<<<<< HEAD
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
=======
    def __init__(self):
        self.board = np.zeros([11,11,1])
        self.GameState = 0
        self.NextPlayer = 1
        self.NextMoveBoard = np.zeros([11,11,1]) #Helps with NN proccessing. This way "self.board" can be inverted without damaging the "MakeMove" and "GetValidMoves" functions, which are needed for the MTCS

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
        temp.reshape(121)
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
        if board[location] == 0 and (player in [PlayerSchema["player1"], PlayerSchema["player2"]]):
            return np.put(board,location,player)
        else:
            raise ValueError('Invalid Input')
    
def GetValidMoves(board):
        """
        Get all valid moves for a given board.
        """
        print(board)
        temp = copy(board)
        temp.reshape(121)
        return np.where(temp == 0)[0]
>>>>>>> 452a54fc44bd98be79d7d874c39ce2367c45627e

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


    def GetGameState(board):
        """
        Returns game state from a given board:
          0: Game has not reached terminal position
          1: Game has reached terminal position with player 1 victory
          2: Game has reached terminal position with player 2 victory
        Input must be of type np.array() with shape (121) and must only contain values of the following:
          0:Empty
          1:Player 1
          2:Player 2
        """
        # Constants
        # PLAYERSTARTS = ((0,1,2,3,4,5,6,7,8,9,10),(0,11,22,33,44,55,66,77,88,99,110))
        # PLAYERDESTS = ((110,111,112,113,114,115,116,117,118,119,120),(10,21,32,43,54,65,76,87,98,109,120))
        # https://github.com/cython/cython/wiki/tutorials-NumpyPointerToC
        # Arrays will become boolean C arrays instead of slow python ones.

        PLAYERSTARTS = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        PLAYERDESTS = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

        # This takes too much computation
        # [1 if x in GLOBAL_CHECKED else 0 for x in range(121)]
        GLOBAL_CHECKED = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        def check_state_from_queue(queue, player):
        LocalChecked = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        new_queue = []
        for position in queue:
            GLOBAL_CHECKED[position]=1
            for neighbor_w in (-11,-10,-1,1,10,11):
            # NP Optimize
            neighbor = position+neighbor_w
            if 0 <= neighbor <= 120 and board[neighbor] == player and GLOBAL_CHECKED[neighbor]==0 and LocalChecked[neighbor]==0:
                if (PLAYERDESTS[player - 1][neighbor]==1 and PLAYERSTARTS[player-1][position]==0) and PLAYERDESTS[player-1][position]==1:
                print('yes',player,neighbor,position)
                # Doesn't work for some reason
                return 1
                new_queue.append(neighbor)
                LocalChecked[neighbor]=1
        if not new_queue:
            return 0
        else:
            check_state_from_queue(new_queue, player)

        if check_state_from_queue((0,1,2,3,4,5,6,7,8,9,10), 1) == 1:
        return 1
        elif check_state_from_queue((0,11,22,33,44,55,66,77,88,99,110), 2) == 1:
        return 2
        else:
        return 0
    
