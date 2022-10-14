import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import numpy as np
from board_maker import board_heat

total_moves, filterable = board_heat()

# Dash code
dash.register_page(__name__)

layout = html.Div(
    children = [
        html.H3('Hans Niemann\'s Square Frequency'),
        dcc.Graph(id="graph"),
        html.H4("Color:"),
        dcc.RadioItems(
            id='color',
            className='radio-class',
            options=['Black', 'White', 'Both'],
            value='Both'
        )
    ]
)

@callback(
    Output("graph", "figure"), 
    Input("color", "value"))
def filter_heatmap(value):
    temp1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    temp2 = ['8', '7', '6', '5', '4', '3', '2', '1']
    if value == "Both":
        fig = px.imshow(total_moves, text_auto=True, labels=dict(color="%"),
                x=temp1,
                y=temp2)
        return fig
    df1 = filterable.loc[filterable['color'] == f"{value}"]
    fig = px.imshow(df1.select_dtypes(include=np.number), text_auto=True, labels=dict(color="%"),
                x=temp1,
                y=temp2)
    return fig
