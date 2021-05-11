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

X_treinamento = pd.read_json(r'dados/X_treinamento.json')
X_treinamento.drop(['horario_experimento', 'mes_experimento', 'vazao_inicial', 'vazao_final', 'vazao_total'], axis=1)

X_teste = pd.read_json(r'dados/X_teste.json')
teste_json = pd.read_json(r'dados/y_teste.json', typ='series')

def make_predictions(model, training, data):

    path_model = 'best_models/' + model + '/model_' + training + '.h5'

    loaded_model = KerasRegressor(build_fn=build_model, verbose=1)
    loaded_model.model = load_model(path_model)

    path_scaler = 'best_models/' + model + '/scaler_' + training + '.joblib'

    scaler = load(path_scaler)

    loaded_steps = [('scaler', scaler), 
                    ('estimator', loaded_model)]

    loaded_pipe = pipeline.Pipeline(loaded_steps)

    predictions = loaded_pipe.predict(data)

    return predictions

def get_precipitation_expected_predicted(array_precipitation):

    result_precipitation = []

    for i in range(array_precipitation.shape[0]):
        dfE = pd.DataFrame(
            array_precipitation[i].reshape(16,16), 
            columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', 
                    '9', '10', '11', '12', '13', '14', '15'])
        w = dfE.values.sum()
        result_precipitation.append(w)

    return result_precipitation

def get_clean_data():
    x_teste_copy = X_teste.copy().drop(['horario_experimento', 'mes_experimento', 'vazao_inicial', 'vazao_final', 'vazao_total'], axis=1)

    b = []
        
    for i in range(teste_json.size):
        b.append(list(teste_json[i]))

    y_teste = np.array(b, dtype='float32')

    return x_teste_copy, y_teste

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
            input_shape=[len(X_treinamento.keys())]
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