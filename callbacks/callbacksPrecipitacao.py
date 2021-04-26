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

experimentos = pd.read_json(r'dados/experimentos.json')

def get_table(filtro_experimento):

    dff = pd.DataFrame.from_dict(np.array(experimentos.iloc[filtro_experimento]['Precipitação']).reshape(16,16))

    dff.reset_index(level=0, inplace=True)
    dff.rename(columns = {'index' : ''}, inplace = True)

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

def get_surface_plot(filtro_experimento):

    z_data = pd.DataFrame.from_dict(np.array(experimentos.iloc[filtro_experimento]['Precipitação']).reshape(16,16))

    fig = go.Figure(
        data=[
            go.Surface(
                z=z_data.values,
                autocolorscale=False,
                colorscale="ice_r",
                showscale=False
            )
        ],
        layout=go.Layout(
                title=str("Superfície de Precipitação"),
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

def get_heatmap(filtro_experimento):

    z_data = pd.DataFrame.from_dict(np.array(experimentos.iloc[filtro_experimento]['Precipitação']).reshape(16,16))

    fig = go.Figure(data=go.Heatmap(
            z=z_data.values,
            colorscale="ice_r",
            showscale=False,
        )
    )

    fig.update_layout(
        title='Precipitação - Mapa de Calor',
        xaxis=dict(nticks=4),
        yaxis=dict(nticks=4),
        width=750,
        height=650,
    )

    hm = dcc.Graph(figure=fig, config={"displayModeBar": False, "showTips": False})

    return hm

def get_perfil_dist(filtro_experimento):

    dff = pd.DataFrame.from_dict(np.array(experimentos.iloc[filtro_experimento]['Precipitação']).reshape(16,16))

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
        title='Perfil de Distribuição de Irrigação',
        xaxis=dict(nticks=8, tick0=1.06, dtick=2.12),
        xaxis_title='Distância',
        yaxis_title='Precipitação(mm/h)',
        width=750,
        height=650,
    )

    perfil = dcc.Graph(figure=fig, config={"displayModeBar": False, "showTips": False})

    return perfil

def get_wind_graph(filtro_experimento):

    dff = pd.DataFrame({'Direção': np.array(experimentos.iloc[filtro_experimento]['dirvento']), 'Velocidade': np.array(experimentos.iloc[filtro_experimento]['velvento'])})

    grp = dff.groupby(["Direção", "Velocidade"]).size().reset_index(name="Frequência")

    fig = px.bar_polar(
        grp, 
        r="Velocidade",
        theta="Direção",
        color="Frequência",
        color_continuous_scale= 'ice_r',
        barmode='group'
    )

    fig.update_layout(
        title="Condições de Vento observadas durante o ensaio",
        width=750,
        height=650,
    )

    wind = dcc.Graph(figure=fig, config={"displayModeBar": False, "showTips": False})

    return wind

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    Input('filtro-experimento', 'value')
)
def switch_tab(active_tab, filtro_experimento):

    if filtro_experimento is None:
        raise PreventUpdate

    if active_tab == "matrix-container":
        return get_table(filtro_experimento-1)

    if active_tab == "prec-heatmap":
        return get_heatmap(filtro_experimento-1)

    if active_tab == "prec-surface":
        return get_surface_plot(filtro_experimento-1)

    if active_tab == "perfil-dist":
        return get_perfil_dist(filtro_experimento-1)

    if active_tab == "wind-pol":
        return get_wind_graph(filtro_experimento-1)
