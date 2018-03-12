from flask import Flask,render_template, request, jsonify
from AI.API import MakeMove
import time
import numpy as np

app = Flask(__name__)



@app.route("/")
def hexgame():
	return render_template('Hexgame.html')

@app.route('/_processrequest', methods=['GET', 'POST'])
def processrequest():
	indata = request.get_json()
	print(indata,time.time())
	output =  MakeMove(computetime = indata['computetime'],board = np.array(indata['board']), humanplayer = indata['humanplayer'])
	print(output,time.time())
	print(type(indata['board']))
	return jsonify(**output)

if __name__ == "__main__":
	app.run(port=80,host= '0.0.0.0')

