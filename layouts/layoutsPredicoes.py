from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd

from callbacks import callbacksPredicoes

X_validacao = pd.read_json(r'dados/X_validacao.json')

options = {}

# result = [(index, experimento, bocal, pressao, quebra_jato, vel_vento, dir_vento) 
#           for index, experimento, bocal, pressao, quebra_jato, vel_vento, dir_vento  in 
#               zip(X_validacao[''], 
#                   X_validacao['Experimento'], 
#                   X_validacao['Bocal'], 
#                   X_validacao['Pressão'],
#                   X_validacao['Quebra Jato'],
#                   X_validacao['Velocidade Vento'],
#                   X_validacao['Direção Vento']
#                  )
#         ]

result = [(bocal, pressao, quebra_jato, vel_vento, dir_vento) 
          for bocal, pressao, quebra_jato, vel_vento, dir_vento  in 
              zip(
                  X_validacao['bocal'], 
                  X_validacao['pressao'],
                  X_validacao['quebra_jato'],
                  X_validacao['vel_vento'],
                  X_validacao['dir_vento']
                 )
        ]

i = 0
for r in result:
    #label = str(r[0]) + " - Experimento: " + str(r[1]) + " Bocal: " + str(r[2]) + " Pressão: " + str(r[3]) + " Quebra Jato: " + str(r[4]) + " Velocidade Vento: " + str(round(r[5], 3)) + " Direção Vento: " + str(round(r[6], 3))
    label = " Bocal: " + str(r[0]) + " Pressão: " + str(r[1]) + " Quebra Jato: " + str(r[2]) + " Velocidade Vento: " + str(round(r[3], 3)) + " Direção Vento: " + str(round(r[4], 3))
    options[i] = label
    i = i+1

layout = html.Div([
    html.H4(children='Realização de Novas Predições e Análise de Resultados'),

    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='filtro-modelos-predicao', 
                    options=[
                        {'label': 'Precipitação - 1 Layer', 'value': 'precipitacao-layer-1'},
                        {'label': 'Precipitação - Melhor Modelo', 'value': 'precipitacao-final'},
                        {'label': 'Coeficiente de Uniformidade - 1 Layer', 'value': 'precipitacao-layer-1'},
                        {'label': 'Coeficiente de Uniformidade - 8 Layers', 'value': 'precipitacao-layer-1'}
                    ],
                    placeholder='Selecione um Modelo',
                    style={'margin-bottom': '5px'}
                ),
            ]),

            dbc.Col([
                dcc.Dropdown(
                    id='filtro-experimento-predicao', 
                    options=[{'label': value, 'value': key} for key, value in options.items()],
                    placeholder='Selecione um Experimento',
                    style={'margin-bottom': '5px'}
                ),
            ], className='col-8')

        ])
    ]),

    html.Div(id='prediction-container')
])