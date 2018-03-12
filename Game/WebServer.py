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
	print('Response at {time}:{data}'.format(time=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f'),data=output))
	return jsonify(**output)

if __name__ == "__main__":
	app.run(port=80,host= '0.0.0.0')

