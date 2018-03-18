from flask import Flask,render_template, request, jsonify
from AI.API import MakeMove
import time
import datetime
import numpy as np

app = Flask(__name__)

@app.route("/")
def hexgame():
	return render_template('Hexgame.html')

@app.route('/_processrequest', methods=['GET', 'POST'])
def processrequest():
	indata = request.get_json()
	print('Request Recived at {time}:{data}'.format(time=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'),data=indata))
	output =  MakeMove(computetime = indata['computetime'],board = np.array(indata['board']), humanplayer = indata['humanplayer'])
	print(output)
	print('Response at {time}:{data}'.format(time=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'),data=output))
	return jsonify(**output)
'''
def parse(board):
	"""
	Returns a potential move history (one that could arive at that board)
	Input, list with length 121.
	"""
	output = []
	cur_1 = 0
	cur_2 = 0
	while cur_2 <= 120 or cur_1 <=120:
		while board[cur_1] != 1 and cur_1 <=120:
			cur_1 += 1
		output.append(cur_1)
		while board[cur_2] != 2 and cur_2 <=120:
			cur_2 += 1
		output.append(cur_2)
	k = output.pop(-1) if output[-1] == 121 else 0
	k = output.pop(-1) if output[-1] == 121 else 0
	return output
'''
if __name__ == "__main__":
	app.run(port=80,host= '0.0.0.0')
