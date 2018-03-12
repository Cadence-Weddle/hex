from HexGame import *
from IdiotBot import *

game = HexGame(gameid="TEST", board=np.array([1 for x in range(120)]))
print(game.check_if_victory(), game.board)