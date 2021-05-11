import pandas as pd

import dash_core_components as dcc
import dash_html_components as html

from callbacks import callbacksModelos

layout = html.Div([
    html.H4(children='Melhores Modelos Encontrados através de processo BayesSearchCV'),

    html.Div([
        dcc.Dropdown(
            id='filtro-modelos', 
            options=[
                {'label': 'Precipitação - 1 Layer', 'value': 'precipitacao-layer-1'},
                {'label': 'Precipitação - 8 Layers', 'value': 'precipitacao-layer-1'},
                {'label': 'Coeficiente de Uniformidade - 1 Layer', 'value': 'precipitacao-layer-1'},
                {'label': 'Coeficiente de Uniformidade - 8 Layers', 'value': 'precipitacao-layer-1'}
            ],
            placeholder='Selecione um Modelo',
            style={'margin-bottom': '5px'}
        ),
    ]),

    html.Div(id='model-container')
])