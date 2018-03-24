import numpy as np
from copy import deepcopy as copy

class Game():
	def __init__(self):
    
		self.board = np.zeros([121])
		self.GameState = 0
		self.NextPlayer = -1 
		self.NextMoveBoard = np.zeros([121]) #Helps with NN proccessing. This way "self.board" can be inverted without damaging the "MakeMove" and "GetValidMoves" functions, which are needed for the MTCS
		self.history = []

	def MakeMove(self, location, player=None):
    """
    Game.MakeMove modfies the array Game.board and Game.NextMoveBoard 
    """
		player = player if player else self.NextPlayer
		MakeMove(self.NextMoveBoard, location, player, PlayerSchema={"player1" : 1, "player2" : -1})
		self.history.append(location)
		self.GameState = GetGameState(self.NextMoveBoard, players=[1,-1])
		self.NextPlayer = SwitchPlayer(self.NextPlayer)
		self.board = self.NextMoveBoard
		if self.NextPlayer == -1:
			self.InvertBoard()


	def GetValidMoves(self):
		if not self.GameState:
				board = self.NextMoveBoard
				return GetValidMoves(board)
    return []

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
		if board[location] == 0 and (player in [PlayerSchema["player1"], PlayerSchema["player2"]]):
			np.put(board,location,player)
		else:
			raise ValueError('Invalid Input. Got [loc : {}, player : {}, board[loc] : {}, \n board : {}'.format(location, player, board[location], board))
	
def GetValidMoves(board):
	"""
	Get all valid moves for a given board.
	"""
	temp = copy(board)
	temp.reshape(121)
	return np.where(temp == 0)[0]

def SwitchPlayer(player,schema=0):
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


def GetGameState(board,players=[1,-1]):
    """
    Returns game state from a given board:
      0: Game has not reached terminal position
      players[0]: Game has reached terminal position with player players[0] victory
      players[1]: Game has reached terminal position with player players[1] victory
    Input must be of type np.array() with shape (121) and must only contain values of the following:
      0:Empty
      players[0]:Player 1
      players[1]:Player 2
    """
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
    GLOBAL_CHECKED = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
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
    WeightPos = [[1, 11], [-1, 1, 10, 11], [-1, 1, 10, 11], [-1, 1, 10, 11], [-1, 1, 10, 11], [-1, 1, 10, 11], [-1, 1, 10, 11], [-1, 1, 10, 11], [-1, 1, 10, 11], [-1, 1, 10, 11], [-1, 11], [-11, -10, 1, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -1, 10, 11], [-11, -10, 1, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -1, 10, 11], [-11, -10, 1, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -1, 10, 11], [-11, -10, 1, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -1, 10, 11], [-11, -10, 1, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -1, 10, 11], [-11, -10, 1, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -1, 10, 11], [-11, -10, 1, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -1, 10, 11], [-11, -10, 1, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -1, 10, 11], [-11, -10, 1, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -10, -1, 1, 10, 11], [-11, -1, 10, 11], [-11, -10, 1], [-11, -10, -1, 1], [-11, -10, -1, 1], [-11, -10, -1, 1], [-11, -10, -1, 1], [-11, -10, -1, 1], [-11, -10, -1, 1], [-11, -10, -1, 1], [-11, -10, -1, 1], [-11, -10, -1, 1], [-1, -11]]
    def check_state_from_queue(queue, _player):
        #print('Player:',player)
        #print('GlobalCheckedBegin:',np.flipud(np.rot90(np.array(GLOBAL_CHECKED).reshape(11,11))))
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
            # print('position',position)
            GLOBAL_CHECKED[position]=1
            # print(WeightPos[position])
            for neighbor_w in WeightPos[position]:
                # NP Optimize
                neighbor = position+neighbor_w
                if board[neighbor] == players[_player] and board[position]==players[_player] and GLOBAL_CHECKED[neighbor]==0 and LocalChecked[neighbor]==0 :
                    #print(player,position,neighbor)
                    if (PLAYERDESTS[_player][neighbor]==1 and PLAYERSTARTS[_player][position]==0) and PLAYERDESTS[_player][position]==0:
                        #print('Win,Player:',player,'Neighbor:',neighbor,'Position:',position)
                        return 1
                    new_queue.append(neighbor)
                    LocalChecked[neighbor]=1
        if not new_queue:
            return 0
        else:
            #print('Q',queue)
            #print('GlobalC',np.flipud(np.rot90(np.array(GLOBAL_CHECKED).reshape(11,11))))
            #print('NQ',new_queue)
            return check_state_from_queue(new_queue, _player)

    if check_state_from_queue((0,1,2,3,4,5,6,7,8,9,10), 0) == 1:
        return players[0]
    else:
        GLOBAL_CHECKED = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
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
        if check_state_from_queue((0,11,22,33,44,55,66,77,88,99,110), 1) == 1:
            return players[1]
        else:
            return 0