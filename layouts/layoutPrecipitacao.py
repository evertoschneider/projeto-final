import pandas as pd

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from callbacks import callbacksPrecipitacao

dados = pd.read_json(r'dados/experimentos.json')

options = {}

result = [(index, experimento, bocal, pressao, quebra_jato) 
          for index, experimento, bocal, pressao, quebra_jato  in 
              zip(dados[''], 
                  dados['Experimento'],
                  dados['Bocal'], 
                  dados['Pressão'],
                  dados['Quebra Jato']
                 )
        ]

for r in result:
    label = "Experimento: {} | Bocal: {} | Pressão: {} | Quebra Jato: {}".format(r[1], r[2], r[3], r[4])
        
    options[r[0]] = label

layout = html.Div([

    html.H4(children='Análise de Precipitação dos Experimentos Realizados'),
    
    html.Div([
        dcc.Dropdown(
            id='filtro-experimento', 
            options=[{'label': value, 'value': key} for key, value in options.items()],
            placeholder='Selecione um Experimento',
            style={'margin-bottom': '5px'}
        ),
    ]),

    html.Div([
        dbc.Tabs(
            [
                dbc.Tab(label="Tabela", tab_id="matrix-container"),
                dbc.Tab(label="Mapa de Calor", tab_id="prec-heatmap"),
                dbc.Tab(label="Superfície de Precipitação", tab_id="prec-surface"),
                dbc.Tab(label="Perfil de Distribuição", tab_id="perfil-dist"),
                dbc.Tab(label="Vento", tab_id="wind-pol")
            ],
            id="tabs",
            active_tab="matrix-container"
        ),
        html.Div(id="tab-content")
    ])
])