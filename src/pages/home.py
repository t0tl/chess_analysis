import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='Home page for navigating to different visualisations'),

    html.Div(children='''
        Press any of the links above.
    '''),

])