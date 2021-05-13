from dash_html_components.Div import Div
import pandas as pd

import dash_core_components as dcc
import dash_bootstrap_components as dbc
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

    html.Div([
        dbc.Tabs([
                dbc.Tab(label="Parâmetros/Avaliação", tab_id="model-parameters"),
                dbc.Tab(label="Análise de Resíduos", tab_id="model-error"),
                dbc.Tab(label="Validação Cruzada", tab_id="model-cv"),
                dbc.Tab(label="Retreinamento Perda/Erro", tab_id="model-loss")
            ],
            id="tabs-models",
            active_tab="model-parameters"
        ),

        html.Div(id='model-container')
    ])
    
])