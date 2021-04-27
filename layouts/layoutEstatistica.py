import pandas as pd

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from callbacks import callbacksEstatistica

dados = pd.read_json(r'dados/experimentos.json')

layout = html.Div([
    html.H4(children='Análise Estatística'),

    html.Div([

        # dbc.Row([
        #     dbc.Col([
        #         dcc.Dropdown(
        #             id='filtro-coluna-x', 
        #             options=[{'label': i, 'value': i} for i in dados.columns],
        #             placeholder='Selecione uma coluna',
        #             style={'margin-bottom': '5px', 'margin-right': '5px'}
        #         ),
        #     ]),

        #     dbc.Col([
        #         dcc.Dropdown(
        #             id='filtro-coluna-y', 
        #             options=[{'label': i, 'value': i} for i in dados.columns],
        #             placeholder='Selecione uma coluna',
        #             style={'margin-bottom': '5px', 'margin-right': '5px'}
        #         ),
        #     ])
        # ]),

        dbc.Tabs([
                dbc.Tab(label="Análise Básica", tab_id="basic-stats"),
                dbc.Tab(label="Gráfico de Dispersão", tab_id="scatter-plot"),
            ],
            id="tabs-stats",
            active_tab="basic-stats"
        ),

        html.Div(id="tab-content-stats")
    ]),

    #html.Div(id="tab-content-stats")
])