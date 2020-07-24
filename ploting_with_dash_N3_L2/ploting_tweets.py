# -*- coding: utf-8 -*-
"""
This script was developed according the course of big data's visualization
of FCS.
In the Level 3 Lesson 1
It was assumed that I'll do with simple HTML and JavaScript, but
I know how to do in that way. So... I decided to explore Dash - Plotly with
Python.

It will be very useful. I recommend you.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import datetime
import plotly.express as px
import pandas as pd
import sys
sys.path.append('./../')
from libs.mongo_lib import Bd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

bd = Bd('localhost', 'aramirez', 'iangelmx', 'test')

BASE = 'tweets_claro'

collection = bd.get_docs( BASE )
df = pd.DataFrame.from_records( collection )

df['created_at'] = df['created_at'].apply( lambda fecha: str(fecha) )
df['text'] = df['text'].apply(lambda x: x.replace('.', '.\n<br>').replace('?', '?\n<br>').replace('!', '!\n<br>').replace('y', 'y\n<br>') )

fig = px.scatter(df, x="likes", y="rts",
                 hover_data=["text", 'created_at'],
                 height=600
)

app.layout = html.Div(children=[
    html.H1(children='Dash Plot'),

    html.Div(children=f'''
        Tweets, likes and Retweets... of {BASE}
    '''),
    dcc.Graph(
        id='religion-mexico',
        figure=fig,
        animate=True
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)