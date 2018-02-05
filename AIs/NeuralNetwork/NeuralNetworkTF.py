import tensorflow as tf

def Conv2D(out_channels, filter_shape, padding):
    filter = tf.Variable(shape=(1) + shape + (out_channels))
    return lambda x: tf.nn.conv2d(x, filter, strides=[1,1,1,1], padding=padding)

def BatchNormalisation():
    return lambda x: tf.nn.batch_normalization(x, ???)

def Activation(type_):
    return lambda x:getattr(tf.nn, type_)(x)

def Dense(output_shape):
    def output(x, output_shape=output_shape):
        bias = tf.Variable(tf.truncated_normal(stddev=0.1, shape=output_shape))
        shape = (x.shape[0], output_shape[1])
        weight = tf.Variable(tf.truncated_normal(stddev=0.1, shape=shape))
        return tf.matmul(x, weight) + bias
    return output

def Input(shape):
    return tf.placeholder(shape=(1) + shape)


class NeuralNetwork:
    def __init__(self, resid_num_iter=15, input_shape=(11,11,3), device="/cpu:0"):
    	#Layer 0 of input is all p1 pos 
    	#Layer 1 of input is all p2 pos
    	#Layer 2 is who's moving

        def residual_section(model):
            output = Conv2D(121, (3, 3), padding='same')(model)
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            output = Conv2D(121, (3, 3), padding='same')(output)
            output = BatchNormalisation()(output)
            output = keras.layers.add([model, output])
            output = Activation('relu')(output)
            return output

        def conv_section(model):
            output = Conv2D(121, (3, 3), padding='same')(model)
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            return output

        def policy_head(model, board_size=11):
            output = Conv2D(121, (1, 1), padding='same')(model)
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            output = Dense(121)(output)
            output = Activation('sigmoid')(output)
            return output

        def value_head(model):
            output = Conv2D(121, (2, 2), padding='same')(model)
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            output = Dense(121)(output)
            output = Activation('relu')(output)
            output = Dense(1)(output)
            output = Activation('tanh')(output)
            return output

        self.resid_num_iter = resid_num_iter

        self.input_data = Input(shape=input_shape)

        self.x = conv_section(self.input_data)

        for _ in range(self.resid_num_iter):
            self.x = residual_section(self.x)

        self.policy = policy_head(self.x)
        self.value  = value_head(self.x)

        self.model = tf.concat(self.policy, self.value)

    def eval(boards, model="model"): # "model" refers to either the policy head, the value head, or both combined. 
        with tf.device(self.device) as device:    
            with tf.Session() as sess:
                return sess.run(getattr(self, model), feed_dict={self.input_data : boards})


    def train_model(self, data, optimiser=SGD(), batch_size=50, epochs=20):
        


if __name__ == "__main__":
    My_model = NeuralNetwork()
    My_model.plot_model(fp='model_architecture.svg')