!pip install dash
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import datetime as dt
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load data from csv
def load_data():
    # To do: Completar la función 
    df = pd.read_csv('DATOSCLIENTE1_.csv')
    df['Fecha']= pd.to_datetime(df['Fecha'])
    df.set_index('Fecha')

    return df
    
# Cargar datos
data = load_data()

app = Dash(__name__)

app.layout = html.Div([
    html.H4('ELECTRO DUNAS'),
    html.H3('Consumo de electricidad segmento industrial'),
    html.P("Medición:"),
    dcc.Dropdown(
        id="ddMedicion",
        options=["A", "B", "C"],
        value="A",
        clearable=False,
    ),
    html.P("Sector:"),
    dcc.Dropdown(
        id="ddSector",
        options=["A", "B", "C"],
        value="A",
        clearable=False,
    ),
    html.P("Cliente:"),
    dcc.Dropdown(
        id="ddCliente",
        options=["Cliente 1", "Cliente 2", "Cliente 3"],
        value="Cliente 1",
        clearable=False,
    ),
    dcc.Graph(id="series"),
])

@app.callback(
    Output("series", "figure"), 
    Input("ddMedicion", "value"))

def display_series(ticker):
    fig = px.line(data, x='Fecha', y=data.columns)

    return fig

app.run_server(debug=True)
