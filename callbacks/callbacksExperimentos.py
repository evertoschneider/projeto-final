import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

from app import app
import pandas as pd

experimentos = pd.read_json(r'dados/experimentos.json')
experimentos = experimentos.drop('Precipitação', axis = 1)

def generate_table(dataframe):
    
    header = []

    for col in dataframe.columns:
        header.append(html.Th(col))

    return dbc.Table(
        # Header
        [html.Thead([
            html.Tr(header)
        ])] +

        # Body
        [html.Tbody([
            html.Tr([
                html.Td(
                    dataframe.iloc[i][col]
                ) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), 20))
        ])],

        #style
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    )

@app.callback(
    Output('table-container', 'children'),
    Input('filtro-bocal', 'value'),
    Input('filtro-pressao', 'value'),
    Input('filtro-quebra-jato', 'value')
)
def display_table(filtro_bocal, filtro_pressao, filtro_quebra_jato):

    if all([param is None for param in [filtro_bocal, filtro_pressao, filtro_quebra_jato]]):
        return generate_table(experimentos)

    dff = experimentos

    if filtro_bocal:
        dff = experimentos[experimentos['Bocal'] == filtro_bocal]

        if (not filtro_pressao) & (not filtro_quebra_jato):
            return generate_table(dff)

    if filtro_pressao:
        dff = dff[dff['Pressão'] == filtro_pressao]

        if (not filtro_bocal) & (not filtro_quebra_jato):
            return generate_table(dff)

    if filtro_quebra_jato:
        dff = dff[dff['Quebra Jato'] == filtro_quebra_jato]

        if (not filtro_bocal) & (not filtro_pressao):
            return generate_table(dff)

    return generate_table(dff)