import tensorflow as tf
from MCTS import MonteCarloTreeSearch as MCTS
from fractions import Fraction
from numpy import sigmoid
import random
import os
import pickle
from Game import HexGame



def var(shape)
	return tf.Variable(tf.truncated_normal(shape, stddev=0.1))

def weight_var(shape):
	return var(shape)
def bias_var(shape):
	return var(shape)
	
def conv(x, W)
	return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding="SAME")


class Bot:
	def __init__(**kwargs):
		self.kwargs = kwargs
		self.x = tf.Placeholder(kwargs.get("imgshape", [11,11,1,1]))
		self.pool = kwargs.get("pool", False)
		self.create_network(kwargs) #ABUSE OF KWARGS

		self.games = 0
		self.wins = 0
		self._update_score()

	def get_score(self):
		try:
			return self.score
		except:
			return 0

	def update_score(self):
		try:	
			self.score = Fraction(self.wins, self.games)
		except:
			return
	def create_network(self, kwargs):
		self.Weight_0 = kwargs.get("weight_0", weight_var([5,5,1, 32], kwargs.get("layer_0_conv_size", 32)))
		self.Bias_0 = kwargs.get("bias_0", bias_var([32]))
		self.conv0 = tf.nn.relu(conv(self.x, self.Weight_0) + Bias_0)
		self.layer_0 = self.pool_test(self.conv0)

		self.Weight_1 = kwargs.get("weight_1", weight_var([5,5,kwargs.get("layer_0_conv_size", 32),kwargs.get("layer_1_conv_size", 32)]))
		self.Bias_1 = kwargs.get("bias_1", bias_var([32]))
		self.conv1 = tf.nn.relu(conv(self.layer_0, self.Weight_1))
		self.layer_1 = self.pool_test(self.conv1)

		self.Weight_2 = kwargs.get("weight_2", weight_var([5,5,kwargs.get("layer_1_conv_size", 32),kwargs.get("layer_2_conv_size", 32)]))
		self.Bias_2 = kwargs.get("bias_2", bias_var([32]))
		self.conv2 = tf.nn.relu(conv(self.layer_0, self.Weight_1))
		self.layer_2 = self.pool_test(self.conv2)

		self.fclw0 = kwargs.get("fully_connected_layer_weights_0", weight_var([1,1,64, 128]))
		self.fclb0 = kwargs.get("fully_connected_layer_bias_0", bias_var([128]))
		self.fclw1 = kwargs.get("fully_connected_layer_weights_1", weight_var([1,1,128, 121]))
		self.fclb1 = kwargs.get("fully_connected_layer_bias_1", bias_var([121]))
		self.fcl0 = tf.nn.relu(tf.MatMul(self.layer_2, self.fclw0) + self.fclb0)
		self.output = tf.nn.softmax(tf.MatMul(self.fcl0, self.fclw1) + self.fclb1)

	def pool_test(layer):
		if self.pool:
			return tf.nn.max_pool(layer, ksize=self.kwargs.get("pool_ksize", [1,2,2,1]), strides=self.kwargs.get("pool_strides", [1,2,2,1]), padding=self.kwargs.get("pool_padding", "SAME"))
		else: return layer

	def predict(board):
		return tf.argmax(tf.Session().run(self.output.predict(feed_dict={self.x: board})))

	def return_weights(self):
		x = ["Weight_0", "Bias_0", "Weight_1", "Bias_1", "Weight_2", "Bias_2", "fcl0w", "fclb0", "fclw1", "fclb1"]
		return [getattr(y, self) for y in x]

	@classmethod
	def from_weights(Bot, weights_0, bias_0, weight_1, bias_1, weights_2, bias_2, fcl0w, fclb0, fclw1, fclb1):
		return Bot(weight_0=weights_0, bias_0=bias_0, weight_1=weights_1, weight_2=weights_2, bias_2=bias_2, fully_connected_layer_weights_0=fcl0w, fully_connected_layer_bias_0=fclb0, fully_connected_layer_weights_1=fclw1, fully_connected_layer_bias_1=fclb1)

def breed(*parents, **kwargs):
	weights_0 = [x.weight_0 for x in parents]
	bias_0 = [x.bias_0 for x in parents]
	weights_1 = [x.weights_1 for x in parents]
	bias_1 = [x.bias_1 for x in parents]
	weights_2 = [x.weights_2 for x in parents]
	bias_2 = [x.bias_2 for x in parents]
	fcl0w = [x.fcl0w for x in parents]
	fclb0 = [x.fclb0 for x in parents]
	fcl1w = [x.fclw1 for x in parents]		
	fclb1 = [x.fclb1 for x in parents]
	return parents, Bot.from_weights(weights_0, bias_0, weights_1, bias_1, weights_2, bias_2, fcl0w, fclb0)

def mutate(parent):
	return parent, Bot.from_weights(*[x + tf.truncated_normal(x.shape, stddev=0.1) for x in parent.return_weights()])

def generation(bots=bots, number=1, **kwargs):
	bot_list = bots
	num_bots = kwargs.get("num_bots", len(bot_list))
	playable_bots = {x : bot_list[x] for x in bot_list}
	for i, bot in enumerate(bot_list):
		del playable_bots[i]
		for opponent in playable_bots.keys():
			result = play_set_of_games(bot, playable_bots[opponent], count=100)
			bot_win = result[0]
			opponent_win = result[1]
			bot.wins += bot_win
			bot_list[opponent].wins += opponent_win
			bot.games += 100
			bot_list[opponent].games += games
	for bot in bot_list:
		bot.update_score()


    #Breeding / Mutation. a bot can do only one. 
	bot_list = sorted(bot_list, key=lamda x: x.score)[::-1]
	bot_list[:num_bots]
	copy_bot_list = []
	for bot in bot_list:
		with tf.Session() as sess:	
			prob = 1 -  sess.run(tf.nn.sigmoid(float(number)))[0]
		if random.choice(prob * 10000 * [1] + (1-prob) * 10000 * [0]): #Choose option with probability sigmoid(number)
			copy_bot_list.append(*mutate(bot))
		else:
			copy_bot_list.append(breed(bot, random.choice(bot_list)))

	return copy_bot_list

def write_generation(bots,index, **kwargs):
	location = kwargs.get("location", "generations\\generation_{}\\".format(str(index)))
	try:
		assert type(index) is str
		assert type(location) is str
		bots[0]
	except:
		raise Exception("Invalid arguments")
	def ensure_dir(file_path):
    	directory = os.path.dirname(file_path)
		if not os.path.exists(directory):
	    	os.makedirs(directory)
	ensure_dir(location)

	record_file = "generation_loader.table"
	record_file = open(record_file, 'a+')
	record_file.write(index + ":" + location + ":" + str(len(bots)) + "\n")
	os.makedir(location)
	for i, bot in enumerate(bots):
		file = open("BOT_{}.pickle".format(i), 'ax')
		pickle.dump(bot, file)
		file.close()
	record_file.close()
	return location

def load_generation(index, **kwargs)
	record_file = kwargs.get(record_file, "generation_loader.table")
	record_file.open(record_file, "r")
	bots = []
	stored_generations = record_file.readlines()
	location_data = [x for x in stored_generations if x.split(":")[0] == number][0].split(":")
	location = location_data[1]
	for i in range(int(location_data[-1])):
		x = open(location + "BOT_{}".format(i), "r")
		bots.append(pickle.load(x))
		x.close()
	record_file.close()
	return bots

def play_game(model1, model2):
	game = HexGame()
	mcts1 = MCTS(policy=model1.output)
	mcts2 = MCTS(policy=model2.output)
