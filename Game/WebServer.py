from flask import Flask,render_template, request, jsonify
from AI.API import _MakeMove_ as MakeMove
from copy import deepcopy as copy
import time
import datetime
import numpy as np
import AI.GameLogic.GameLogic as GameLogic
app = Flask(__name__)

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
        output = MakeMove(computetime = indata['computetime'], board = curr_board)
        print('Response at {time}:{data}'.format(time=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f') ,data=output))
        return jsonify(**output)

if __name__ == "__main__":
	    app.run(host='0.0.0.0', port=80, threaded=True)

