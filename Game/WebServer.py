from flask import Flask,render_template, request, jsonify
from AI.API import MakeMove
from copy import deepcopy as copy
import time
import datetime
import numpy as np
import AI.GameLogic.GameLogic as GameLogic
import AI.NeuralNetwork.NeuralNetwork as NeuralNetwork
import AI.TreeSearch.MonteCarloTreeSearch as MonteCarloTreeSearch

NN = NeuralNetwork.NeuralNetwork
MCTS = MonteCarloTreeSearch.MonteCarloTreeSearch
NNBP = MonteCarloTreeSearch.Neural_Network_Batch_Processer
Game = GameLogic.Game


class MCTS_Manager:
	def __init__(self):
		self.game = Game()
		self.nn = NN()
		self.nnbp = NNBP(self.nn)
		self.mcts = MCTS(self.game, processer=self.nnbp)
	
	def MakeMove(self, board, computetime):
		"""
		Performs Monte Carlo Tree Search from a specific board, with a specific amount of time for computation. 
		"""
		history = self.gen_history(board)
		mcts = self.mcts
		mcts.execute_history(history)
		RootNodePointer = mcts.root_node 
		move = mcts.turn(computetime)
		RootNodePointer[move].parent = RootNodePointer
		return {'moveloc' : str(move), 'gamestate' : str(RootNodePointer[move].game.GameState)}
	
	def gen_history(board):
	    """
	    Returns a possible history of moves that could have led to that state. 
	    """
	    board = np.array(board)
	    p1 = np.where(board == 1)
	    p2 = np.where(board == 2)
	    lesser = min(len(p1),len(p2))
	    return np.stack((p2[0][:lesser],p1[0][:lesser])).flatten('F')


app = Flask(__name__)
MCTSM = MCTS_Manager()

@app.route("/")
def hexgame():
	return render_template('Hexgame.html')

@app.route('/processrequest', methods=['GET', 'POST'])
def processrequest():
	indata = request.get_json()
	curr_board = np.array(indata['board'])
	#Check if Game Has Reached Terminal State
	if GameLogic.GetGameState(curr_board)==0:
		return jsonify({'gamestate':0})
	else:
		output =  MCTSM.MakeMove(computetime = indata['computetime'], board = curr_board)
		print('Response at {time}:{data}'.format(time=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'),data="-"))
		return jsonify(**output)

if __name__ == "__main__":
	app.run(port=80,host= '0.0.0.0', threaded=True)
