from app import app

import pandas as pd
import numpy as np

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

dados = pd.read_json(r'dados/dataframe-clusters.json')

def get_clusters(dataframe):

    if dataframe is None:
        raise PreventUpdate

    df = dataframe

    fig = px.scatter(
        df,
        x="Componente 1",
        y="Componente 2",
        color="Cluster Predito",
        hover_data=['Bocal', 'Pressão', 'Quebra Jato', 'Velocidade Vento', 
                    'Direção Vento', 'CUC 12x12', 'CUC 12x15', 'CUC 15x15'],
        color_continuous_scale=('rgb(3, 5, 18)', 'rgb(72, 134, 187)', 'rgb(114, 184, 205)')
    )

    row = dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig, config={"displayModeBar": False, "showTips": False})
            ])
        ])

    return row

@app.callback(
    Output('clusters-content', 'children'),
    Input('clusters-bocal', 'value'),
    Input('clusters-pressao', 'value'),
    Input('clusters-quebra-jato', 'value')
)
def display_table(filtro_bocal, filtro_pressao, filtro_quebra_jato):

    dff = dados

    if all([param is None for param in [filtro_bocal, filtro_pressao, filtro_quebra_jato]]):
        return get_clusters(dff)

    if filtro_bocal:
        dff = dff[dff['Bocal'] == filtro_bocal]

        if (not filtro_pressao) & (not filtro_quebra_jato):
            return get_clusters(dff)

    if filtro_pressao:
        dff = dff[dff['Pressão'] == filtro_pressao]

        if (not filtro_bocal) & (not filtro_quebra_jato):
            return get_clusters(dff)

    if filtro_quebra_jato:
        dff = dff[dff['Quebra Jato'] == filtro_quebra_jato]

        if (not filtro_bocal) & (not filtro_pressao):
            return get_clusters(dff)

    return get_clusters(dff)
    