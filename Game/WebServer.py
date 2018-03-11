from flask import Flask,render_template, request, jsonify
from AI.Controller import MakeMove
import time

app = Flask(__name__)

@app.route("/")
def hexgame():
	return render_template('Hexgame.html')

@app.route('/_processrequest', methods=['GET', 'POST'])
def processrequest():
	indata = request.get_json()
	print(indata,time.time())

	output =  MakeMove(computetime = indata['computetime'],board = indata['board'], humanplayer = indata['humanplayer'])
	print(output,time.time())

	return jsonify(**output)

if __name__ == "__main__":
	app.run(port=80)

