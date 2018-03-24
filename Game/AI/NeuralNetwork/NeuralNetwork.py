import tensorflow as tf
import keras
from keras.layers import Activation, BatchNormalization, Conv2D, Input, Dense, Add, Flatten
from keras.utils import plot_model
from keras.optimizers import SGD
from keras.models import Model
from keras.callbacks import TensorBoard
from keras.losses import categorical_crossentropy
import numpy as np
import keras.backend as k

def NNCreater(nn):
    n = NeuralNetwork()
    n.model = nn
    print(n)
    return n

class NeuralNetwork:
    def __init__(self, resid_num_iter=10, input_shape=(11,11, 1), optimizer='Adam'):
        #Layer 0 of input is all p1 pos 
        #Layer 1 of input is all p2 pos
        #Layer 2 is who's moving
        
        self.resid_num_iter = resid_num_iter        
        self.input_shape = input_shape


        def add_residual_section(model,):
            output = Conv2D(1, (3, 3,), padding='same')(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            output = Conv2D(1, (3, 3,), padding='same')(output)
            output = BatchNormalization()(output)
            output = keras.layers.add([model, output])
            output = Activation('relu')(output)
            return output

        def add_conv_section(model,n_filters=1,n_kernel_size=(3, 3)):
            output = Conv2D(filters=n_filters,
                            kernel_size=n_filters,
                            padding='same')(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            return output

        def add_policy_head(model, board_size=11):
            output = Conv2D(1, (1, 1,), padding='same')(model)
            output = BatchNormalization()(output)
            output = Flatten()(output)
            output = Activation('relu')(output)
            output = Dense(board_size ** 2)(output)
            output = Activation('sigmoid',name='policy_output')(output)
            return output

        def add_value_head(model):
            output = Conv2D(1, (2, 2), padding='same')(model)
            output = BatchNormalization()(output)
            output = Flatten()(output)
            output = Activation('relu')(output)
            output = Dense(1)(output)
            output = Activation('relu')(output)
            output = Dense(1)(output)
            output = Activation('tanh', name='value_output')(output)
            return output

        self.input_layer = Input(shape=input_shape)

        self.model_layers = add_conv_section(self.input_layer)


        for _ in range(self.resid_num_iter):
            self.model_layers = add_residual_section(self.model_layers)

        self.policy_output = add_policy_head(self.model_layers)
        self.value_output = add_value_head(self.model_layers)

        self.model = Model(inputs=[self.input_layer], outputs=[self.policy_output, self.value_output])
        self.model.compile(optimizer=optimizer, loss={'policy_output':'categorical_crossentropy','value_output':'binary_crossentropy'})

    def plot_model(self, fp='model.png'):
        '''
        Outputs a flowchart of model
        '''
        plot_model(self.model, to_file=fp)

    def foward_prop(self,data, BatchSize=32):
        '''
        Works with batches

        If a single value:
        Returns dictionary with the following:
        policy: coordinates of gamesquare as per standard in a 2-tuple
        value: a floating point value which is the estimate of the value of the game

        If multiple values:
        Returns a list of dictonaries that follow the same scheme as single valued
        '''

        #if len(data.shape)==4:
        #This could be made more efficent
        if type(data) != np.array:
            data = np.array(data)
        output_data = self.model.predict(np.array(data), batch_size=BatchSize)

        ___ = range(len(output_data[0]))
        policies = [output_data[0][i] for i in ___]
        #        policies_argmax = [np.argmax(output_data[0][i]) for i in ___]
        values = [output_data[1][i][0] for i in ___]
        return [(p,v) for p,v in zip(policies, values)]
        


    def train_model(self, input_data, value_output_data, policy_output_data, epochs=10,batch_size=64):
        '''
        input_data is a game board of shape as specified in shape. Should be a 4D array
        value output should be a 3D array with shape (-1,1,121)
        policy output is a 2D array with shape (-1,1)
        '''

        '''
        try:
            assert(len(input_data) == len(value_output_data) == len(policy_output_data))
        except AssertionError:
            raise Exception("Length(x)={} but Length(y)={}. Invalid data".format(len(x), len(y)))
        '''
        #print(input_data.shape, value_output_data.shape, policy_output_data.shape)
        #print(input_data[0], value_output_data[0], policy_output_data[0])
        #policy_output_data = policy_output_data.reshape([len(input_data), 121, 1])
        self.model.fit(x=input_data, y={'policy_output':policy_output_data,'value_output':value_output_data}, batch_size=batch_size, epochs=epochs)
