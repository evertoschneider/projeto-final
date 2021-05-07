import pandas as pd

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from callbacks import callbacksClusters

dados = pd.read_json(r'dados/dataframe-clusters.json')

layout = html.Div([

    dbc.Row([
        html.H4(children='Análise de Clusters/PCA dos Experimentos Realizados')
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='clusters-bocal', 
                options=[{'label': i, 'value': i} for i in dados["Bocal"].unique()],
                placeholder='Tipo de Bocal',
                style={'margin-bottom': '5px', 'margin-right': '5px'}
            ),
        ]),

        dbc.Col([
            dcc.Dropdown(
                id='clusters-pressao', 
                options=[{'label': i, 'value': i} for i in dados["Pressão"].unique()],
                placeholder='Valor de Pressão',
                style={'margin-bottom': '5px', 'margin-right': '5px'}
            ),
        ]),

        dbc.Col([
            dcc.Dropdown(
                id='clusters-quebra-jato', 
                options=[{'label': i, 'value': i} for i in dados["Quebra Jato"].unique()],
                placeholder='Tipo de Quebra Jato',
                style={'margin-bottom': '5px'}
            ),
        ]),
    ]),

    html.Div(id="clusters-content")
])