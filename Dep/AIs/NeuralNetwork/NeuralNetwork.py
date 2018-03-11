import tensorflow as tf
import keras
from keras.layers import Activation, BatchNormalization, Conv2D, Input, Dense
from keras.utils import plot_model
from keras.optimizers import SGD



class NeuralNetwork:
    def __init__(self, resid_num_iter=10, input_shape=(11,11,3)):
        #Layer 0 of input is all p1 pos 
        #Layer 1 of input is all p2 pos
        #Layer 2 is who's moving
        
        self.resid_num_iter = resid_num_iter        
    	
        def addd_residual_section(model):
            output = Conv2D(121, (3, 3,), padding='same', data_format=(None, 11,11,1))(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            output = Conv2D(121, (3, 3,), padding='same')(output)
            output = BatchNormalization()(output)
            output = keras.layers.add([model, output])
            output = Activation('relu')(output)
            return output

        def add_conv_section(model, input_shape):
            output = Conv2D(121, (3, 3,), padding='same', data_format=input_shape)(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            return output

        def add_policy_head(model, board_size=11):
            output = Conv2D(121, (1, 1,), padding='same', data_format=(11,11,1))(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            output = Dense(board_size ** 2)(output)
            output = Activation('sigmoid')(output)
            return output

        def add_value_head(model):
            output = Conv2D(121, (2, 2), padding='same', data_format=(11,11,1))(model)
            output = BatchNormalization()(output)
            output = Activation('relu')(output)
            output = Dense(121)(output)
            output = Activation('relu')(output)
            output = Dense(1)(output)
            output = Activation('tanh')(output)
            return output

        self.input_layer = Input(shape=input_shape)

        self.model_layers = add_conv_section(self.input_layer, input_shape)



        for _ in range(self.resid_num_iter):
            self.model_layers = add_residual_section(self.model_layers)

        self.policy_output = add_policy_head(self.model_layers)
        self.value_output = add_value_head(self.model_layers)

        self.model = Model(inputs=[self.input_layer], outputs=[self.policy_output, self.value_output])
        self.input_shape = input_shape







    def plot_model(self, fp='model.png'):
        plot_model(self.model, to_file=fp)

    def foward_prop(object):
        shape=board.shape
        if shape != (11,11,3):
            board.reshape(11,11,3)
        return model.predict(board) #Probably won't work, I likely need to format the data. 

    def propogate_policy_head():
        return None


    def propogate_value_head():
        return None

    def predict_batch(batch):
        if batch[0].shape != self.input_shape:
            for x in batch:x.reshape((11,11))
        return self.model.predict(batch, batch_size=len(batch))


    def train_model(self, data, optimiser=SGD(), batch_size=50, epochs=20, **kwargs):
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