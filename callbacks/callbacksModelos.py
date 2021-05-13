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

def get_table_model(filtro_modelo, tipo_tabela):

    path = 'best_models/' + filtro_modelo + '/best_model_' + tipo_tabela + '.json'

    loaded_table = pd.read_json(path)

    tb = dbc.Table(
        # Header
        [html.Tr([html.Th(col) for col in loaded_table.columns])] +

        # Body
        [html.Tr([
            html.Td(loaded_table.iloc[i][col]) for col in loaded_table.columns
        ]) for i in range(0, len(loaded_table))],

        #style,
        size='sm',
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    )

    return tb

def update_title_layout(title):
    return {
            'text': title,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
        }

def get_model_loss(filtro_modelo):

    history = pd.read_json('best_models/' + filtro_modelo + '/history')
    history.reset_index(inplace=True)
    history = history.rename(columns = {'index':'epoch'})

    hist_erro = px.line(history, x="epoch", y="mse")
    hist_erro.update_yaxes(
        range=[0, 2]
    )

    hist_loss = px.line(history, x="epoch", y="loss")
    hist_loss.update_yaxes(
        range=[0, 2]
    )

    result = html.Div([
        dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=hist_erro, config={"displayModeBar": False, "showTips": False})
                ]),

                dbc.Col([
                    dcc.Graph(figure=hist_loss, config={"displayModeBar": False, "showTips": False})
                ])
            ])
        ])

    return result

def get_model_error(filtro_modelo):

    x_teste, y_teste = loadModelFunctions.get_clean_data()

    predictions = loadModelFunctions.make_predictions(filtro_modelo, '70_30', x_teste)
    
    expected_precipitation = loadModelFunctions.get_precipitation_expected_predicted(y_teste)
    predicted_precipitation = loadModelFunctions.get_precipitation_expected_predicted(predictions)

    error = pd.Series(np.array(expected_precipitation) - np.array(predicted_precipitation))

    hist = go.Figure(
        go.Histogram(
            x=error,
            xbins=dict(start=-150, end=150, size=15),
            nbinsx=7
        )
    )

    hist.update_layout(
        title= update_title_layout('Distribuição dos Resíduos - Histograma'),
        xaxis_title="Resíduos",
        yaxis_title="Observações",
        bargap=0.1
    )

    hist.update_xaxes(
        range=[-150, 150],
        nticks=7
    )

    resultados = pd.DataFrame({'Valores Preditos':predicted_precipitation, 'Resíduos':error})

    scatter = px.scatter(resultados, x='Valores Preditos', y='Resíduos')
    scatter.add_hline(0, line_dash="dash")

    scatter.update_layout(
        title= update_title_layout('Gráfico de Dispersão dos Resíduos')
    )

    result = html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=hist, config={"displayModeBar": False, "showTips": False})
            ]),

            dbc.Col([
                dcc.Graph(figure=scatter, config={"displayModeBar": False, "showTips": False})
            ])
        ]),
    ])

    return result


def get_table_parameters(filtro_modelo):
    tb_metrics = get_table_model(filtro_modelo, 'metrics')
    tb_params = get_table_model(filtro_modelo, 'params')

    result = html.Div([
        dbc.Row([
            dbc.Col([
                tb_metrics
            ]),

            dbc.Col([
                tb_params
            ])
        ]),
    ])

    return result

@app.callback(
    Output('model-container', 'children'),
    Input('filtro-modelos', 'value'),
    Input('tabs-models', 'active_tab')
)
def generate_model_evaluation(filtro_modelo, active_tab):

    if filtro_modelo is None and active_tab is None:
        raise PreventUpdate

    if active_tab is not None and filtro_modelo is None:
        return html.P('Selecione um modelo acima para carregar sua análise')

    if active_tab == "model-parameters":
        return get_table_parameters(filtro_modelo)

    if active_tab == "model-error":
        return get_model_error(filtro_modelo)

    #model-cv

    if active_tab == "model-loss":
        return get_model_loss(filtro_modelo)