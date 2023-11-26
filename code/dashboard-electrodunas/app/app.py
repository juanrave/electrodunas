from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
import json
from loguru import logger
import os

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]

# app server
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# PREDICTION API URL 
api_url = os.getenv('API_URL')
api_url = "http://{}:8001/api/v1/predict".format(api_url)


# App layout
app.layout = dbc.Container([
    dbc.Row([ 
      html.Div(children="ELECTRO DUNAS", className="d-block p-2 bg-primary text-white fs-1")
    ]),
    dbc.Row([
      html.Div(children="Consumo de electricidad segmento industrial", className="d-block p-2 bg-dark text-white fs-3")
    ]),
        dbc.Row([
      html.Div(children="Detección de perdidas no técnicas", className="d-block p-2 bg-dark text-white fs-5")
    ]),
    dbc.Row([
        dbc.Col([
          dbc.Label("Cliente:", className="fw-normal"),
          dcc.Dropdown(id='cliente-dropdown', options=['CLIENTE1', 'CLIENTE2', 'CLIENTE3', 'CLIENTE4', 'CLIENTE5', 'CLIENTE6', 'CLIENTE7', 'CLIENTE8', 'CLIENTE9', 'CLIENTE10'], value='CLIENTE1')
        ], width=2),
        dbc.Col([
          dbc.Label("Acumular por:", className="fw-normal"),
          dcc.Dropdown(id='medida-dropdown', options=['Mínimo', 'Máximo', 'Media', 'No acumular'], value='Media')
        ], width=2),
        dbc.Col([
          dbc.Label("Energia activa:", className="fw-normal"),
          dcc.Input(
              id="energia-input",
              placeholder="Ingrese la energía activa",
              max=0,
              min=100,
              step=0.01
          )
        ], width=2),
        dbc.Col([
            html.Div(id="resultado-output", className="fs-1 fw-bold")
        ], width=2)
    ]),
    dbc.Row([
        dbc.Col([   
            html.Div(id="consumo-table")     
        ], width=4),
        dbc.Col([
            dcc.Graph(figure={}, id='consumo-graph')
        ], width=6),
    ]),
  ], fluid=True)

@app.callback(
    [Output("consumo-table", "children"),
    Output(component_id='consumo-graph', component_property='figure')],
    [Input("cliente-dropdown", "value"),
     Input("medida-dropdown", "value")]
)
def update_output(cliente, medida):
    url = f'https://raw.githubusercontent.com/juanrave/electrodunas/main/datos/DATOS{cliente}.csv'
    df = pd.read_csv(url, sep=',')
    
    df['Periodo'] = df['Fecha'].str.slice(0, 7).str.replace("-", "")

    match medida:
      case 'Mínimo':
        data = df.groupby(['Periodo'])['Active_energy'].min()
        data = data.to_frame()
        data = data.reset_index()
        data.columns = ['Periodo', 'Active_energy']
      case 'Máximo':
        data = df.groupby(['Periodo'])['Active_energy'].max()
        data = data.to_frame()
        data = data.reset_index()
        data.columns = ['Periodo', 'Active_energy']
      case "Media":
        data = df.groupby(['Periodo'])['Active_energy'].mean()
        data = data.to_frame()
        data = data.reset_index()
        data.columns = ['Periodo', 'Active_energy']
      case _:
        data = df[['Periodo', 'Active_energy']]

    fig = px.line(data, x='Periodo', y='Active_energy')

    return html.Div(
        [
            dash_table.DataTable(
                data=data.to_dict("rows"),
                columns=[{"id": x, "name": x} for x in data.columns],
                page_size= 10,
            )
        ]
    ), fig

# Method to update prediction
@app.callback(
    Output("resultado-output", "children"),
    Input("energia-input", "value")
)
def update_output(energia):
    myreq = {
        "inputs": [
            {
            "Customer_Age": 57,
            "Gender": "M",
            "Dependent_count": 4,
            "Education_Level": "Graduate",
            "Marital_Status": "Single",
            "Income_Category": "$120K +",
            "Card_Category": "Blue",
            "Months_on_book": 52,
            "Total_Relationship_Count": int(servicios),
            "Months_Inactive_12_mon": int(inactivo),
            "Contacts_Count_12_mon": 2,
            "Credit_Limit": 25808,
            "Total_Revolving_Bal": 0,
            "Avg_Open_To_Buy": 25808,
            "Total_Amt_Chng_Q4_Q1": 0.712,
            "Total_Trans_Amt": int(transac),
            "Total_Trans_Ct": int(num_transac),
            "Total_Ct_Chng_Q4_Q1": 0.843,
            "Avg_Utilization_Ratio": 0
            }
        ]
      }
    headers =  {"Content-Type":"application/json", "accept": "application/json"}

    # POST call to the API
    response = requests.post(api_url, data=json.dumps(myreq), headers=headers)
    data = response.json()
    logger.info("Response: {}".format(data))

    # Pick result to return from json format
    result = "ALTO riesgo de perdidas" if round(data["predictions"][0])==1 else "BAJO riesgo de perdidas"
    
    return result 

if __name__ == "__main__":
    logger.info("Running dash")
    app.run_server(debug=False)
