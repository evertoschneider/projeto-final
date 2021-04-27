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

# def get_scatter_graph():

#     return ""


# def get_dist_graphs(filtro_coluna, filtro_coluna_y):

#     bocal = go.Figure(
#         go.Histogram(
#             x=experimentos[filtro_coluna],
#             xbins=get_hist_bins(filtro_coluna)
#         )
#     )

#     bocal.update_layout(
#         title= update_layout("Histograma")
#     )

#     box = px.box(
#         experimentos,
#         y=filtro_coluna,
#         title="Box-Plot",
#         points="all"
#     )

#     box.update_layout(
#         title= update_layout("Box-Plot")
#     )

#     marg = px.scatter(
#         experimentos,
#         x=filtro_coluna,
#         y=filtro_coluna_y
#     )

#     marg.update_layout(
#         # xaxis_title="",
#         yaxis_title= "" if filtro_coluna_y == None else filtro_coluna_y,
#         title= update_layout("Dispersão")
#     )

#     graph = html.Div([

#         dbc.Row([
#             dbc.Col([
#                 dcc.Graph(figure=bocal, config={"displayModeBar": False, "showTips": False})
#             ]),
#             dbc.Col([
#                 dcc.Graph(figure=box, config={"displayModeBar": False, "showTips": False})
#             ]),
#             dbc.Col([
#                 dcc.Graph(figure=marg, config={"displayModeBar": False, "showTips": False})
#             ])
#         ])
#     ], id="tab-content-stats-x")

#     return graph

# @app.callback(
#     Output("tab-content-stats-x", "children"),
#     Input('filtro-coluna-x', 'value'),
#     Input('filtro-coluna-y', 'value')
# )
# def get_stats_y(filtro_coluna_x, filtro_coluna_y):

#     if filtro_coluna_y is None:
#         raise PreventUpdate

#     return get_dist_graphs(filtro_coluna_x, filtro_coluna_y)

# @app.callback(
#     Output("tab-content-stats", "children"),
#     Input('filtro-coluna-x', 'value'),
#     Input('filtro-coluna-y', 'value'),
# )
# def get_stats_x(filtro_coluna_x, filtro_coluna_y):

#     if filtro_coluna_x is None and filtro_coluna_y is None:
#         raise PreventUpdate

#     if filtro_coluna_x == filtro_coluna_y:
#         filtro_coluna_y = None

#     return get_dist_graphs(filtro_coluna_x, filtro_coluna_y)


def get_scatter_plot():

    filter = html.Div([

        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='filtro-scatter-x', 
                    options=[{'label': i, 'value': i} for i in experimentos.columns],
                    placeholder='Selecione uma coluna',
                    style={'margin-top': '5px', 'margin-bottom': '5px', 'margin-right': '5px'}
                ),
            ]),

            dbc.Col([
                dcc.Dropdown(
                    id='filtro-scatter-y', 
                    options=[{'label': i, 'value': i} for i in experimentos.columns],
                    placeholder='Selecione uma coluna',
                    style={'margin-top': '5px', 'margin-bottom': '5px', 'margin-right': '5px'}
                ),
            ])
        ]),

        html.Div(id='scatter-div')
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

    tab = go.Figure(go.Table(
        cells=dict(values=[experimentos[filtro_coluna].describe().index, experimentos[filtro_coluna].describe()],
                align='left'))
    )

    tab.update_layout(
        title= update_layout("Resumo Numérico")
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
                dcc.Graph(figure=tab, config={"displayModeBar": False, "showTips": False})
            ]),
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

    if active_tab == "scatter-plot":
        return get_scatter_plot()