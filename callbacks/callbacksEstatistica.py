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

def get_scatter_graph():

    return ""

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

def get_dist_graphs(filtro_coluna, filtro_coluna_y):

    bocal = go.Figure(
        go.Histogram(
            x=experimentos[filtro_coluna],
            xbins=get_hist_bins(filtro_coluna)
        )
    )

    bocal.update_layout(
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

    marg = px.scatter(
        experimentos,
        x=filtro_coluna,
        y=filtro_coluna_y
    )

    marg.update_layout(
        # xaxis_title="",
        yaxis_title= "" if filtro_coluna_y == None else filtro_coluna_y,
        title= update_layout("Dispersão")
    )

    graph = html.Div([

        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=bocal, config={"displayModeBar": False, "showTips": False})
            ]),
            dbc.Col([
                dcc.Graph(figure=box, config={"displayModeBar": False, "showTips": False})
            ]),
            dbc.Col([
                dcc.Graph(figure=marg, config={"displayModeBar": False, "showTips": False})
            ])
        ])
    ], id="tab-content-stats-x")

    return graph

@app.callback(
    Output("tab-content-stats-x", "children"),
    Input('filtro-coluna-x', 'value'),
    Input('filtro-coluna-y', 'value')
)
def get_stats_y(filtro_coluna_x, filtro_coluna_y):

    if filtro_coluna_y is None:
        raise PreventUpdate

    return get_dist_graphs(filtro_coluna_x, filtro_coluna_y)

@app.callback(
    Output("tab-content-stats", "children"),
    Input('filtro-coluna-x', 'value'),
    Input('filtro-coluna-y', 'value'),
)
def get_stats_x(filtro_coluna_x, filtro_coluna_y):

    if filtro_coluna_x is None and filtro_coluna_y is None:
        raise PreventUpdate

    if filtro_coluna_x == filtro_coluna_y:
        filtro_coluna_y = None

    return get_dist_graphs(filtro_coluna_x, filtro_coluna_y)
