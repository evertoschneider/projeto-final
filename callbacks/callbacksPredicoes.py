from app import app
import pandas as pd
import numpy as np

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import plotly.express as px
import plotly.graph_objects as go

from callbacks import loadModelFunctions

def make_perfil_predicao(dff, tipo):

    diag = pd.Series([dff.iat[n, n] for n in range(len(dff))], index=[dff.index, dff.columns])
    inv_diag = pd.Series([dff.iat[x, y] for x,y in zip(range(len(dff)),range(len(dff)-1, -1,-1))], index=[dff.index, dff.columns])

    diags = np.array_split(diag, 2)
    inv_diags = np.array_split(inv_diag, 2)

    qas = [] 
    qbs = []
    qcs = []
    qds = []
    for (a, b, c, d) in zip(
        range(len(diags[0])-1, -1,-1),
        range(len(inv_diags[0])-1, -1,-1),
        range(len(inv_diags[1])),
        range(len(diags[1]))
    ):
        qas.append(round(diags[0].iloc[a], 3)/2)
        qbs.append(round(inv_diags[0].iloc[b], 3)/2)
        qcs.append(round(inv_diags[1].iloc[c], 3)/2)
        qds.append(round(diags[1].iloc[d], 3)/2)

    linevalues = []
    for i in range(len(qas)):
        linevalues.append(np.mean([qas[i], qbs[i], qcs[i], qds[i]]))

    precipitacao = np.array(linevalues)
    distancia = np.array([1.06, 3.18, 5.3, 7.42, 9.54, 11.66, 13.78, 15.9])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
                        x=distancia,
                        y=precipitacao,
                        line=dict(color='rgb(62, 109, 178)'),
                        hoverinfo="y",
                        line_shape='spline'
                    )
                )

    fig.update_layout(
        title='Perfil de Distribuição de Irrigação - ' + tipo,
        xaxis=dict(nticks=8, tick0=1.06, dtick=2.12),
        xaxis_title='Distância',
        yaxis_title='Precipitação(mm/h)',
        width=750,
        height=650,
    )

    perfil = dcc.Graph(figure=fig, config={"displayModeBar": False, "showTips": False})

    return perfil

def get_perfil_predicao(dfE, dfP):

    div_surfaces = dbc.Row([
        dbc.Col([
            make_perfil_predicao(dfE, "Valores Reais")
        ]),

        dbc.Col([
            make_perfil_predicao(dfP, "Valores Preditos")
        ]),
    ])

    return div_surfaces

def make_surface_predicao(dff, tipo):
    fig = go.Figure(
        data=[
            go.Surface(
                z=dff.values,
                autocolorscale=False,
                colorscale="ice_r",
                showscale=False
            )
        ],
        layout=go.Layout(
                title=str("Superfície de Precipitação - " + tipo),
                width=650,
                height=650,
                scene = dict(
                            xaxis = dict(
                                showspikes=False,
                                spikesides=False,
                                showaxeslabels=False,
                                title=dict(text='')
                            ),
                            yaxis = dict(
                                showspikes=False,
                                spikesides=False,
                                showaxeslabels=False,
                                title=dict(text='')
                            ),
                            zaxis = dict(
                                showspikes=False,
                                spikesides=False,
                                showaxeslabels=False,
                                title=dict(text='')
                            )
                        )
            ),
    )

    camera = dict(
        eye=dict(y=1.5, z=2.0)
    )
    fig.update_layout(scene_camera=camera)
    
    sup = dcc.Graph(figure=fig, config={"displayModeBar": False, "showTips": False})

    return sup

def get_surface_predicao(dfE, dfP):

    div_surfaces = dbc.Row([
        dbc.Col([
            make_surface_predicao(dfE, "Valores Reais")
        ]),

        dbc.Col([
            make_surface_predicao(dfP, "Valores Preditos")
        ]),
    ])

    return div_surfaces

def make_table_predicao(dff):
    tb = dbc.Table(
        # Header
        [html.Tr([html.Th(col) for col in dff.columns])] +

        # Body
        [html.Tr([
            html.Td(dff.iloc[i][col].round(decimals=3)) for col in dff.columns
        ]) for i in range(0, len(dff))],

        #style,
        size='sm',
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    )

    return tb

def get_tables_predicao(dfE, dfP):

    div_tables = dbc.Row([
        dbc.Col([
            html.H5(children='Valores Reais de Precipitação'),
            make_table_predicao(dfE)
        ]),

        dbc.Col([
            html.H5(children='Valores Preditos de Precipitação'),
            make_table_predicao(dfP)
        ]),
    ])

    return div_tables

def get_expected_predicted(filtro_modelo, filtro_experimento):

    x = loadModelFunctions.X_validacao.loc[filtro_experimento].values.reshape(1,-1)
    y = loadModelFunctions.y_validacao[filtro_experimento]

    prediction = loadModelFunctions.make_predictions(filtro_modelo, x)

    dfE = loadModelFunctions.get_precipitation_expected_predicted(y)
    dfP = loadModelFunctions.get_precipitation_expected_predicted(prediction)

    dfE.reset_index(level=0, inplace=True)
    dfE.rename(columns = {'index' : ''}, inplace = True)

    dfP.reset_index(level=0, inplace=True)
    dfP.rename(columns = {'index' : ''}, inplace = True)

    return dfE, dfP

@app.callback(
    Output('prediction-container', 'children'),
    Input('filtro-modelos-predicao', 'value'),
    Input('filtro-experimento-predicao', 'value')
)
def get_predictions(filtro_modelo, filtro_experimento):

    if filtro_modelo is None or filtro_experimento is None:
        return PreventUpdate

    expected, prediction = get_expected_predicted(filtro_modelo, filtro_experimento)

    div_tables = get_tables_predicao(expected, prediction)

    expected = expected.drop([''], axis = 1)
    prediction = prediction.drop([''], axis = 1)

    div_surface = get_surface_predicao(expected, prediction)
    div_perfil = get_perfil_predicao(expected, prediction)

    div_predicoes = html.Div([
        div_tables,
        div_surface,
        div_perfil
    ], className='mt-5')

    return div_predicoes