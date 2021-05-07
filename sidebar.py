import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from appStyle import SIDEBAR_STYLE, CONTENT_STYLE

sidebar = html.Div(
    [
        html.H2("Projeto Final", className="display-7"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Página Inicial", href="/", active="exact"),
                dbc.NavLink("Experimentos", href="/experimentos", active="exact"),
                dbc.NavLink("Análise de Precipitação", href="/precipitacao", active="exact"),
                dbc.NavLink("Análise Estatística - Dados", href="/estatistica", active="exact"),
                dbc.NavLink("Clusters", href="/clusters", active="exact"),
                dbc.NavLink("Análise Preditiva - Modelos", href="/modelos", active="exact"),
                dbc.NavLink("Análise Preditiva - Predições", href="/predicao", active="exact")
            ],
            vertical=True,
            pills=True
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)