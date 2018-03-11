from flask import Flask,render_template, request, jsonify
app = Flask(__name__)

@app.route("/")
def hexgame():
	return render_template('Hexgame.html')

@app.route('/_processrequest', methods=['GET', 'POST'])
def processrequest():
	indata = request.get_json()
	print(indata['computetime'])

	
	return jsonify(moveloc=95,gamestate=0)

if __name__ == "__main__":
	app.run(port=80)

