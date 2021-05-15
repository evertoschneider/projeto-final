import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras

from tensorflow.keras import layers
from tensorflow.keras import models

from tensorflow.keras.models import load_model
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor

from keras.constraints import maxnorm

from sklearn import pipeline
from joblib import load

X_validacao = pd.read_json(r'dados/X_validacao.json')

validacao_json = pd.read_json (r'dados/Y_validacao.json', typ='series')

a = []

for i in range(validacao_json.size):
    a.append(list(validacao_json[i]))

y_validacao = np.array(a, dtype='float32')


def make_predictions(model, data):

    path_model = 'best_models/' + model + '/model_100.h5'

    loaded_model = KerasRegressor(build_fn=build_model, verbose=1)
    loaded_model.model = load_model(path_model)

    path_scaler = 'best_models/' + model + '/scaler_100.joblib'

    scaler = load(path_scaler)

    loaded_steps = [('scaler', scaler), 
                    ('estimator', loaded_model)]

    loaded_pipe = pipeline.Pipeline(loaded_steps)

    predictions = loaded_pipe.predict(data)

    return predictions

def get_precipitation_expected_predicted(array_precipitation):

    df = pd.DataFrame(
            array_precipitation.reshape(16,16), 
            columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', 
                    '9', '10', '11', '12', '13', '14', '15'])
        
    for i in range(16):
        df.loc[df[str(i)] < 0, str(i)] = 0

    return df


def build_model(
    optimizer,
    init_mode,
    activation,
    dropout_rate,
    weight_constraint,
    neurons,
    loss,
    regularizers
):
    model = models.Sequential()
    
    # layer 1
    model.add(
        layers.Dense(
            neurons,
            activation = activation,
            kernel_initializer=init_mode,
            kernel_constraint=maxnorm(weight_constraint),
            kernel_regularizer=regularizers,
            input_shape=[len(X_validacao.keys())]
        )
    )
    model.add(layers.Dropout(dropout_rate))
    
    # layer 2
    model.add(layers.Dense(256))
    
    model.compile(
        loss=loss,
        optimizer=optimizer,
        metrics=['mae', 'mse', keras.metrics.RootMeanSquaredError()]
    )
    
    return model