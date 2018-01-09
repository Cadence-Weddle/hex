import tensorflow as tf
import keras
from keras.layers import Activation, BatchNormalization, Conv2D, Input, Dense
'''
from keras.layers import BatchNormalization
from keras.layers import Conv2D
from keras.layers import Input
from keras.layers import Dense
'''
from keras.models import Model
from keras.utils import plot_model
from keras.optimizers import SGD



class NeuralNetwork:
    def __init__(self, resid_num_iter=15, input_shape=(11,11,1)):
        def residual_section(model):
            output = Conv2D(256, (3, 3), padding='same')(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            output = Conv2D(256, (3, 3), padding='same')(output)
            output = BatchNormalization()(output)
            output = keras.layers.add([model, output])
            output = Activation('relu')(output)
            return output

        def conv_section(model):
            output = Conv2D(256, (3, 3), padding='same')(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            return output

        def policy_head(model, board_size=11):
            output = Conv2D(2, (1, 1), padding='same')(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            output = Dense(board_size ** 2)(output)
            output = Activation('sigmoid')(output)
            return output

        def value_head(model):
            output = Conv2D(1, (2, 2), padding='same')(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            output = Dense(256)(output)
            output = Activation('relu')(output)
            output = Dense(1)(output)
            output = Activation('tanh')(output)
            return output

        self.resid_num_iter = resid_num_iter

        self.input_data = Input(shape=input_shape)

        self.x = conv_section(self.input_data)

        for _ in range(self.resid_num_iter):
            self.x = residual_section(self.x)

        self.policy_output = policy_head(self.x)
        self.value_output = value_head(self.x)

        self.model = Model(inputs=[self.input_data], outputs=[self.policy_output, self.value_output])


    def plot_model(self, fp='model.png'):
        plot_model(self.NeuralNetworkModel, to_file=fp)

    def predict(board):
        shape=board.shape
        if shape != (11,11,1):
            board.reshape(11,11,1)
        return model.predict(board) #Probably won't work, I likely need to format the data. 


     def train_model(self, data, optimiser=SGD(), batch_size=50 epochs=20):
        model = self.model
        x, y = data[0], data[1]
        try:
            assert(len(x) == len(y))
        except AssertionError:
            raise Exception("Length(x)={} but Length(y)={}. Invalid data".format(len(x), len(y))) 
        epochs = kwargs.get("epochs", len(x) / batch_size)
        model.compile(optimizer=optimiser, loss=kwargs.get("loss", "categorical_crossentropy"), metrics=["accuracy"])
        model.fit(x, y, batch_size=len(x))
        return model


if __name__ == "__main__":
    My_model = NeuralNetwork()
    My_model.plot_model(fp='model_architecture.svg')