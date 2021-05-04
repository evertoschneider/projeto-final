from app import app

import pandas as pd

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

experimentos = pd.read_json(r'dados/experimentos.json')
experimentos_distancia = pd.read_json(r'dados/experimentos-distancia.json')

experimentos = experimentos.drop(['Experimento', 'dirvento', 'velvento', 'Precipitação'], axis = 1)

@app.callback(
    Output('scatter-plot', 'children'),
    Input('filtro-scatter-x', 'value'),
    Input('filtro-scatter-y', 'value')
)
def update_scatter_plot(filtro_x, filtro_y):

    if filtro_x is None or filtro_y is None:
        raise PreventUpdate

    dff = experimentos_distancia

    fig = px.scatter_3d(dff, x=filtro_x, y=filtro_y, z='CUC', color='Distância')

    camera = dict(
        eye=dict(y=1.5, z=2.0)
    )

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', scene_camera=camera)

    fig.update_xaxes(title=filtro_x, type='linear')
    fig.update_yaxes(title=filtro_y, type='linear')

    row = dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig, config={"displayModeBar": False, "showTips": False})
            ])
        ])

    return row

def get_scatter_plot():

    filter = html.Div([

        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='filtro-scatter-x', 
                    options=[{'label': i, 'value': i} for i in experimentos_distancia.columns],
                    placeholder='Selecione uma coluna',
                    style={'margin-top': '5px', 'margin-bottom': '5px', 'margin-right': '5px'}
                ),
            ]),

            dbc.Col([
                dcc.Dropdown(
                    id='filtro-scatter-y', 
                    options=[{'label': i, 'value': i} for i in experimentos_distancia.columns],
                    placeholder='Selecione uma coluna',
                    style={'margin-top': '5px', 'margin-bottom': '5px', 'margin-right': '5px'}
                ),
            ])
        ]),

        html.Div(id='scatter-plot')
    ])

    return filter

@app.callback(
    Output('basic-group-stats-div', 'children'),
    Input('filtro-group-x', 'value'),
    Input('filtro-group-dist', 'value')
)
def filter_basic_group_stats(filtro_coluna, filtro_distancia):

    if filtro_coluna is None or filtro_distancia is None:
        raise PreventUpdate

    dff = experimentos

    data = []
    colors = px.colors.sequential.ice
    
    if filtro_coluna == 'Velocidade Vento' or filtro_coluna == 'Direção Vento':

        for i in range(3, len(experimentos[filtro_coluna].describe())-1):

            stats = experimentos[filtro_coluna].describe()
            mask = (experimentos[filtro_coluna] >= stats[i]) & (experimentos[filtro_coluna] < stats[i+1])
            trace = go.Box(
                        y=experimentos[mask][filtro_distancia],
                        name = str(str(filtro_coluna) + ": " + str(round(stats[i], 3)) + " - " + str(round(stats[i+1], 3))),
                        marker = dict(
                            color = colors[i],
                        )
                    )
            
            data.append(trace)
    else:
        valores_unicos = experimentos[filtro_coluna].unique()
        i = 0

        for u in valores_unicos:
            trace = go.Box(
                y=dff.loc[dff[filtro_coluna] == u][filtro_distancia],
                name = str(str(filtro_coluna) + " - " + str(u)),
                marker = dict(
                    color = colors[i],
                )
            )

            i = i+1
            data.append(trace)
    
    fig = go.Figure(data=data)

    row = dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig, config={"displayModeBar": False, "showTips": False})
        ])
    ])

    return row

def get_basic_group_stats():

    filter = html.Div([

        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='filtro-group-x', 
                    options=[
                        {'label': 'Bocal', 'value': 'Bocal'},
                        {'label': 'Pressão', 'value': 'Pressão'},
                        {'label': 'Quebra Jato', 'value': 'Quebra Jato'},
                        {'label': 'Velocidade Vento', 'value': 'Velocidade Vento'},
                        {'label': 'Direção Vento', 'value': 'Direção Vento'}
                        
                    ],
                    placeholder='Selecione uma coluna',
                    style={'margin-top': '5px', 'margin-bottom': '5px', 'margin-right': '5px'}
                ),
            ]),

            dbc.Col([
                dcc.Dropdown(
                    id='filtro-group-dist', 
                    options=[
                        {'label': '12x12', 'value': 'CUC 12x12'},
                        {'label': '12x15', 'value': 'CUC 12x15'},
                        {'label': '15x15', 'value': 'CUC 15x15'}
                    ],
                    placeholder='Selecione uma distância',
                    style={'margin-top': '5px', 'margin-bottom': '5px', 'margin-right': '5px'}
                ),
            ])
        ]),

        html.Div(id='basic-group-stats-div')
    ])

    return filter

def update_layout(title):
    return {
        'text': title,
        'y': 0.95 if title == "Distribuição Marginal" else 0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }

def get_hist_bins(filtro_coluna):
    if filtro_coluna == "Bocal" or filtro_coluna == "Pressão" or filtro_coluna == "Quebra Jato":
        return dict(start=0, end=5, size=0.1)
    else:
        return None

def get_basic_graphs(filtro_coluna):

    medidas = ['N° Registros', 'Média', 'Desvio Padrão', 'Valor Mínimo', 'Quartil 1', 'Quartil 2', 'Quartil 3', 'Valor Máximo']
    valores = experimentos[filtro_coluna].describe()

    result = pd.DataFrame({'Medidas': medidas, 'Valores': valores})
    result.reset_index(drop=True, inplace=True)

    tb = dbc.Table(
        # Header
        [html.Tr([html.Th(col) for col in result.columns])] +

        # Body
        [html.Tr([
            html.Td(result.iloc[i][col]) for col in result.columns
        ]) for i in range(0, len(result))],

        #style,
        size='sm',
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    )

    hist = go.Figure(
        go.Histogram(
            x=experimentos[filtro_coluna],
            xbins=get_hist_bins(filtro_coluna)
        )
    )

    hist.update_layout(
        title= update_layout("Histograma")
    )

    box = px.box(
        experimentos,
        y=filtro_coluna,
        title="Box-Plot",
        points="all"
    )

    box.update_layout(
        title= update_layout("Box-Plot")
    )

    row = dbc.Row([
            dbc.Col([
                tb
            ], className='mt-5'),
            dbc.Col([
                dcc.Graph(figure=hist, config={"displayModeBar": False, "showTips": False})
            ]),
            dbc.Col([
                dcc.Graph(figure=box, config={"displayModeBar": False, "showTips": False})
            ])
        ])

    return row

@app.callback(
    Output('basic-stats-div', 'children'),
    Input('filtro-basic-stats', 'value')
)
def filter_basic_graphs(filtro_coluna):

    if filtro_coluna is None:
        raise PreventUpdate

    return get_basic_graphs(filtro_coluna)


def get_basic_stats():

    filter = html.Div([

        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='filtro-basic-stats', 
                    options=[{'label': i, 'value': i} for i in experimentos.columns],
                    placeholder='Selecione uma coluna',
                    style={'margin-top': '5px', 'margin-bottom': '5px', 'margin-right': '5px'}
                ),
            ])
        ]),

        html.Div(id='basic-stats-div')
    ])

    return filter

@app.callback(
    Output("tab-content-stats", "children"),
    Input("tabs-stats", "active_tab")
)
def switch_tab_stats(active_tab):

    if active_tab == "basic-stats":
        return get_basic_stats()

    if active_tab == "basic-group-stats":
        return get_basic_group_stats()

    if active_tab == "scatter-plot":
        return get_scatter_plot()