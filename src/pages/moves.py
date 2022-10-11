import chess.pgn
import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
from boardMaker import board_heat, df_to_perc

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

pgn = open("src/niemann_yottabase.pgn")
black = []
white = []
tmp = chess.pgn.read_game(pgn)
while(tmp is not None):
    if tmp.headers["White"] == "Niemann, Hans Moke":
        white.append(tmp)
    else:
        black.append(tmp)
    tmp = chess.pgn.read_game(pgn)

heat_data_white = board_heat(white, 1)
heat_data_black = board_heat(black, 0)

df = pd.DataFrame(data = heat_data_white)
df2 = pd.DataFrame(data = heat_data_black)


df3 = df + df2
df = df_to_perc(df)
df2 = df_to_perc(df2)
df3 = df_to_perc(df3)

df = df.assign(color = ["White", "White","White","White","White","White","White","White"])
df2 = df2.assign(color = ["Black", "Black", "Black","Black","Black","Black","Black","Black"])
df = pd.concat([df, df2])

@callback(
    Output("graph", "figure"), 
    Input("color", "value"))
def filter_heatmap(value):
    temp1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    temp2 = ['8', '7', '6', '5', '4', '3', '2', '1']
    if value == "Both":
        fig = px.imshow(df3, text_auto=True, labels=dict(color="%"),
                x=temp1,
                y=temp2)
        return fig
    df1 = df.loc[df['color'] == f"{value}"]
    fig = px.imshow(df1.select_dtypes(include=np.number), text_auto=True, labels=dict(color="%"),
                x=temp1,
                y=temp2)
    return fig
