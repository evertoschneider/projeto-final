from app import app
import pandas as pd
import numpy as np

import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from callbacks import loadModelFunctions

def get_table_model(filtro_modelo, tipo_tabela):

    path = 'best_models/' + filtro_modelo + '/best_model_' + tipo_tabela + '.json'

    loaded_table = pd.read_json(path)

    tb = dbc.Table(
        # Header
        [html.Tr([html.Th(col) for col in loaded_table.columns])] +

        # Body
        [html.Tr([
            html.Td(loaded_table.iloc[i][col]) for col in loaded_table.columns
        ]) for i in range(0, len(loaded_table))],

        #style,
        size='sm',
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    )

    return tb

@app.callback(
    Output('model-container', 'children'),
    Input('filtro-modelos', 'value')
)
def generate_model_evaluation(filtro_modelo):

    if filtro_modelo is None:
        raise PreventUpdate

    #get metrics
    tb_metrics = get_table_model(filtro_modelo, 'metrics')
    
    #get params
    tb_params = get_table_model(filtro_modelo, 'params')

    x_teste, y_teste = loadModelFunctions.get_clean_data()
    
    #predict model create function
    predictions = loadModelFunctions.make_predictions(filtro_modelo, '70_30', x_teste)
    
    #predicted values create single function to both (pass array)
    expected_precipitation =  loadModelFunctions.get_precipitation_expected_predicted(y_teste)
    predicted_precipitation = loadModelFunctions.get_precipitation_expected_predicted(predictions)

    error = pd.Series(np.array(expected_precipitation) - np.array(predicted_precipitation))

    #load hist graph

    #calculate error
    
    #load normal graphs

    #load cv graphs

    result = html.Div([
        dbc.Row([
            dbc.Col([
                tb_metrics
            ]),

            dbc.Col([
                tb_params
            ])
        ])
    ])

    return result