import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from sidebar import sidebar, content

from app import app
from layouts import layoutExperimentos, layoutModelos, layoutPrecipitacao, layoutEstatistica, layoutsClusters, layoutsPredicoes

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    content
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/":
        return html.P("Página Inicial descrevendo o objetivo do projeto e qual é o conteúdo de cada página [TO DO]")
    elif pathname == "/experimentos":
        return layoutExperimentos.layout
    elif pathname == "/precipitacao":
        return layoutPrecipitacao.layout
    elif pathname == "/estatistica":
        return layoutEstatistica.layout
    elif pathname == "/clusters":
        return layoutsClusters.layout
    elif pathname == "/modelos":
        return layoutModelos.layout
    elif pathname == "/predicao":
        return layoutsPredicoes.layout

    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=True)