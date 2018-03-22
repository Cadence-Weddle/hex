import AI.TreeSearch.MonteCarloTreeSearch as MonteCarloTreeSearch
import AI.GameLogic.GameLogic as GameLogic
import AI.NeuralNetwork.NeuralNetwork as NeuralNetwork
#Curently broken
import sys
import keras
NN = NeuralNetwork.NeuralNetwork
Game = GameLogic.Game
MCTS = MonteCarloTreeSearch.MonteCarloTreeSearch

filepath = sys.argv[2]
iter = sys.argv[1]

nn = keras.models.load_model(filepath)

def gen_match(model):
	mcts = MCTS(Game(), model)
	while not mcts.game.GameState:
		mcts.turn(500)
	return mcts.train(0.99)

def run(iter, filepath):
	for i in range(int(str(iter))):
		print("Started iter {}".format(i))

		iData = []
		pData = []
		vData = []
		print("Beginning self play...")
		d = gen_match(nn)
		print("Self play over")
		iData += d[0]
		pData += d[1]
		vData += d[2]
		print("Training model...")
		nn.train_model(np.array(iData), np.array(vData), np.array(pData))
		print("Training iter done")
		if i % 5 == 0:
			print("Saving model at {}".format(filepath))
			model.save(filepath)
			print("Model Saved")
		print("Finished iter {}".format(i))
	input("Done~$")
	if input("Run again[Y/n]").lower() == "y":
		run()
	return
run(iter, filepath)