from flask import Flask
import json
from AI_V2.AI import Player #MAGIKAL solution to all of the problems | To be implemented
import numpy as np

app = Flask(__name__)
player = Player() #Does something

@app.route("/get_move", methods=["POST"])
def move():
	board = parse(request.board)
	move = player.move(board)




def parse(board):
	"Takes in a board in whatever format from the client and returns a [1, 11, 11, 2] array"
	pass