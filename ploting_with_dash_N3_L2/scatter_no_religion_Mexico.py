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
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('religion.csv')

fig = px.scatter(df, x="Rango_Edades", y="Personas",
                 #size="Rango_Edades",
                 color="Sexo", 
                 hover_name="Estado",
                 #log_x=True, 
                 size_max=60)

app.layout = html.Div([
    dcc.Graph(
        id='religion-mexico',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)