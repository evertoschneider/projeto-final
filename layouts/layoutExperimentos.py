import dash_core_components as dcc
import dash_html_components as html

from callbacks import callbacksExperimentos
import pandas as pd

experimentos = pd.read_json(r'dados/experimentos.json')
experimentos = experimentos.drop('Precipitação', axis = 1)

layout = html.Div([

    html.H4(children='Experimentos Realizados'),
    
    html.Div([
        dcc.Dropdown(
            id='filtro-bocal', 
            options=[{'label': i, 'value': i} for i in experimentos["Bocal"].unique()],
            placeholder='Tipo de Bocal',
            style={'margin-bottom': '5px', 'margin-right': '5px'}
        ),

    ], style={'width': '33%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='filtro-pressao', 
            options=[{'label': i, 'value': i} for i in experimentos["Pressão"].unique()],
            placeholder='Valor de Pressão',
            style={'margin-bottom': '5px', 'margin-right': '5px'}
        ),

    ], style={'width': '33%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='filtro-quebra-jato', 
            options=[{'label': i, 'value': i} for i in experimentos["Quebra Jato"].unique()],
            placeholder='Tipo de Quebra Jato',
            style={'margin-bottom': '5px'}
        ),

    ], style={'width': '34%', 'display': 'inline-block'}),

    html.Div(id='table-container')
])