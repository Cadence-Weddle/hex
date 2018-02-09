import tensorflow as tf

def Conv2D(model, out_channels, filter_shape, padding):
    filter = tf.Variable(tf.truncated_normal(shape=filter_shape + tuple([model.shape[3].value]) + tuple([out_channels]))) #Possibly move tf.cast elsewhere, it may take up extra resources. 
    return tf.nn.conv2d(model, filter, strides=[1,1,1,1], padding=padding)

def BatchNormalisation():
    return lambda x: tf.nn.batch_normalization(x, 0, 1, 0.001, .99, 0.01) #These numbers are magikkal. I don't know what they should be

def Activation(type_):
    return lambda x:getattr(tf.nn, type_)(x)

def Dense(output_shape):
    def output(x, output_shape=output_shape):
        return tf.layers.dense(x, output_shape)
    return output

def Input(shape):
    return tf.placeholder(tf.float32, shape=(1,) + shape)


class NeuralNetwork:
    def __init__(self, resid_num_iter=15, input_shape=(11,11,3), device="/cpu:0"):
    	#Layer 0 of input is all p1 pos 
    	#Layer 1 of input is all p2 pos
    	#Layer 2 is who's moving

        def residual_section(model):
            output = Conv2D(model, 121, (3, 3), padding='SAME')
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            output = Conv2D(output, 121, (3, 3), padding='SAME')
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            return output

        def conv_section(model):
            output = Conv2D(model, 121, (3, 3), padding='SAME')
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            return output

        def policy_head(model, board_size=11):
            output = Conv2D(model, 121, (1, 1), padding='SAME')
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            output = Dense(121)(output)
            output = Activation('sigmoid')(output)
            return output

        def value_head(model):
            output = Conv2D(model, 121, (2, 2), padding='SAME')
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            output = Dense(121)(output)
            output = Activation('relu')(output)
            output = Dense(1)(output)
            output = Activation('tanh')(output)
            return output
        self.device = device
        self.resid_num_iter = resid_num_iter

        self.input_data = Input(shape=input_shape)

        self.x = conv_section(self.input_data)

        for _ in range(self.resid_num_iter):
            self.x = residual_section(self.x)

        self.policy = policy_head(self.x)
        self.value  = value_head(self.x)

        self.model = None #To be implmented. Probably need "tf.stack" or "tf.concat" but I am not sure and don't want to deal with it.

    def eval(self, boards, model="model"): # "model" refers to either the policy head, the value head, or both combined. 
        with tf.device(self.device) as device:    
            with tf.Session() as sess:
                return sess.run(getattr(self, model), feed_dict={self.input_data : boards})


    def train_model(self, data, optimiser='sgd', batch_size=50, epochs=20):
        pass
