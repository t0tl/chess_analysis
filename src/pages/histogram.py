import dash
from dash import html, dcc
import psycopg2
import pandas as pd
import plotly.express as px
from config import config

dash.register_page(__name__)

params = config()
conn = psycopg2.connect(**params)
conn.autocommit = True

# create a cursor
cur = conn.cursor()
cur.execute('''
            SELECT accuracy, 'White' AS color
            FROM niemann
            WHERE white = 'Niemann, Hans Moke'

            UNION

            SELECT accuracy, 'Black' AS color
            FROM niemann
            WHERE black = 'Niemann, Hans Moke';
            ''')

df = pd.DataFrame(cur.fetchall(), columns = ['Accuracy', 'Color'])                       
cur.close()
conn.close()

fig = px.histogram(df, x='Accuracy',
                    color= 'Color',
                    labels={
                     'y': 'Count',
                     'x': 'Accuracy'
                    },
                    facet_col='Color', 
                    color_discrete_sequence=['#262626', '#c2c2c2'], 
                    ).update_layout(yaxis_title="Count", showlegend=False) 
fig.for_each_annotation(lambda a: a.update(text=a.text.replace("Color=", "")))
fig.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Count")))

layout = html.Div(children=[
    html.H3(children='Distribution of Hans Niemann\'s Accuracy per Game'),
	html.Div([
        dcc.Graph(figure=fig),
    ]),
	html.Br(),
    html.Div(),
])