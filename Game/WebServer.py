from flask import Flask,render_template, request, jsonify
from AI.API import MakeMove
from copy import deepcopy as copy
import time
import datetime
import numpy as np
import AI.GameLogic.GameLogic as GameLogic
import AI.NeuralNetwork.NeuralNetwork as NeuralNetwork
import AI.TreeSearch.MonteCarloTreeSearch as MonteCarloTreeSearch
import threading

NN = NeuralNetwork.NeuralNetwork
MCTS = MonteCarloTreeSearch.MonteCarloTreeSearch
NNBP = MonteCarloTreeSearch.Neural_Network_Batch_Processer
Game = GameLogic.Game

class evaluater:
	def __init__(self, root_node,nnbp,  board, computetime):
		self.mcts = MCTS(Game(), nnbp)
		self.board = board
		self.computetime = computetime
	def run(self):
		self.mcts.execute_history(gen_history(self.board))
		move = self.mcts.turn(computetime, False)
		game = self.mcts.game
		return {'moveloc' : move, 'gamestate' : game.GameState}

class MCTS_Manager:
    def __init__(self):
        self.game = Game()
        self.nn = NN()
        self.nnbp = NNBP(self.nn)
        self.mcts = MCTS(self.game, processer=self.nnbp)
    
    def MakeMove(self, board, computetime):
        """
		Dispatchs evaluater objects to threads. 	
	    """
        return evaluater(self.mcts.top, self.mcts.batch_processer, board, computetime)
    
def gen_history(board):
        """
        Returns a possible history of moves that could have led to that state. 
        """
        board = np.array(board)
        p1 = np.where(board == 1)[0]
        p2 = np.where(board == 2)[0]
        lesser = min(len(p1),len(p2))
        return np.stack((p2[:lesser],p1[:lesser])).flatten('F')


app = Flask(__name__)
MCTSM = MCTS_Manager()

@app.route("/")
def hexgame():
    return render_template('Hexgame.html')

@app.route('/_processrequest', methods=['GET', 'POST'])
def processrequest():
    indata = request.get_json()
    curr_board = np.array(indata['board'])
    #Check if Game Has Reached Terminal State
    gamestate = GameLogic.GetGameState(curr_board)
    if gamestate !=0:
        print('Terminal Gamestate Reached')
        return jsonify(gamestate=gamestate)
    else:
        output = MCTSM.MakeMove(computetime = indata['computetime'], board = curr_board).run()
        print('Response at {time}:{data}'.format(time=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f') ,data=output))
        return jsonify(**output)

if __name__ == "__main__":
	    app.run(host='0.0.0.0', port=80, threaded=True)

