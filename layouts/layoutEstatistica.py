import pandas as pd

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from callbacks import callbacksEstatistica

dados = pd.read_json(r'dados/experimentos.json')

layout = html.Div([
    html.H4(children='Análise Estatística'),

    html.Div([

        dbc.Tabs([
                dbc.Tab(label="Análise Básica - Individual", tab_id="basic-stats"),
                dbc.Tab(label="Análise Básica - Por Grupo", tab_id="basic-group-stats"),
                dbc.Tab(label="Gráfico de Dispersão", tab_id="scatter-plot"),
            ],
            id="tabs-stats",
            active_tab="basic-stats"
        ),

        html.Div(id="tab-content-stats")
    ]),

    #html.Div(id="tab-content-stats")
])