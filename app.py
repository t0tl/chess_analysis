import chess.pgn
import plotly.express as px
import numpy as np
from dash import Dash, dcc, html, Input, Output
import pandas as pd
from boardMaker import board_heat, df_to_perc

app = Dash(__name__)

app.layout = html.Div([
    html.H1('All moves in Hans Niemann carrer'),
    dcc.Graph(id="graph"),
    html.P("Color:"),
    dcc.RadioItems(
        id='color',
        options=['black', 'white', 'both'],
        value='both')
])

pgn = open("niemann_yottabase.pgn")
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

df = df.assign(color = ["white", "white","white","white","white","white","white","white"])
df2 = df2.assign(color = ["black", "black", "black","black","black","black","black","black"])
df = pd.concat([df, df2])

# For the future, when hover over position should give
# proportion of pieces who moved there
# Can be implemented using multiple dfs.

@app.callback(
    Output("graph", "figure"), 
    Input("color", "value"))
def filter_heatmap(value):
    temp1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    temp2 = ['8', '7', '6', '5', '4', '3', '2', '1']
    if value == "both":
        fig = px.imshow(df3, text_auto=True, labels=dict(color="%"),
                x=temp1,
                y=temp2)
        return fig
    df1 = df.loc[df['color'] == f"{value}"]
    fig = px.imshow(df1.select_dtypes(include=np.number), text_auto=True, labels=dict(color="%"),
                x=temp1,
                y=temp2)
    return fig

app.run_server(debug=True)