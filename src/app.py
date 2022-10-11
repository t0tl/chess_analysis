import dash
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.H1('Hans Niemann\'s Career Visualised', className="app-header--title")
        ]
    ),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
            ]
        ),
        dash.page_container
])

app.run_server(debug=True)
