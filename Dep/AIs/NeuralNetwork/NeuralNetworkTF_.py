import tensorflow as tf
import numpy as np


def testing(model, attr, correct_errors=True):
    pass

def Conv2D(model, out_channels, filter_shape, padding, name=None):
    filter = tf.Variable(tf.truncated_normal(shape=filter_shape + tuple([model.shape[3].value]) + tuple([out_channels])), ) #Possibly move tf.cast elsewhere, it may take up extra resources. 
    return tf.nn.conv2d(model, filter, strides=[1,1,1,1], padding=padding)

def BatchNormalisation():
    return lambda x: tf.nn.batch_normalization(x, 0, 1, 0.001, .99, 0.01) #These numbers are magikkal. I don't know what they should be

def Activation(type_):
    with tf.Session() as sess:sess.run(tf.global_variables_initializer())
    return lambda x:getattr(tf.nn, type_)(x)

def Dense(output_shape):
    def output(x, output_shape=output_shape):
        return tf.layers.dense(x, output_shape)
    return output

def Input(shape):
    return tf.placeholder(tf.float32, shape=(1,) + shape)

def residual_section(model):
            output = Conv2D(model, 121, (3, 3), padding='SAME')
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            output = Conv2D(output, 121, (3, 3), padding='SAME', )
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            output += model
            return output

def conv_section(model):
                output = Conv2D(model, 121, (3, 3), padding='SAME')
                output = BatchNormalisation()(output)
                output = Activation('relu')(output)
                return output

def policy_head(model, board_size=11):
            output = Conv2D(model, 121, (1, 1), padding='SAME', )
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
            output = Dense(121)(output)
            output = Activation('sigmoid')(output)
            return output

def conv_section(model):
            output = Conv2D(model, 121, (3, 3), padding='SAME')
            output = BatchNormalisation()(output)
            output = Activation('relu')(output)
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

def create_network(resid_num_iter=15, input_shape=(11,11,3)):
    	#Layer 0 of input is all p1 pos 
    	#Layer 1 of input is all p2 pos
    	#Layer 2 is who's moving
        
        input_data = Input(shape=input_shape)

        x = conv_section(input_data)

        for _ in range(resid_num_iter):
            x = residual_section(x)

        policy = policy_head(x)
        value  = value_head(x)
        return policy, value, input_data

    
def eval(boards, model, device, input_data): # "model" refers to either the policy head, the value head, or both combined. 
        with tf.device(device) as device:    
            with tf.Session() as sess:
                return sess.run(model, feed_dict={input_data : boards})


def train_model(self, data, optimiser='sgd', batch_size=50, epochs=20):
        pass

def main():
    p, v, i = create_network()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
    print("Testing Policy")
    eval([np.ones([11,11,3])], p, "/gpu:0", i)
    print("Test complete\nTesting value")
    eval([np.ones([11,11,3])], v, "/gpu:0", i)
