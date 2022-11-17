# Import modules
import dash
from dash import dcc, html
from dash_elements.graph import size_graph, time_graph, token_value_over_time, transactions_graph
from dotenv import load_dotenv
import json
import numpy as np
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash_extensions import Lottie       # pip install dash-extensions
from dash_extensions.enrich import DashProxy
import urllib
from pandas import json_normalize
import requests
from datetime import date
from pathlib import Path
import os

from controllers.token_controller import TokenController
from controllers.polygon_api_controller import token_value, value_over_time
from controllers.block_controller import block_number, blocks_prop, block_transactions_count

SIZE = 100
DAYS = 365

# Initiate the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP])

#polygonscan api call matic supply
load_dotenv()
POLYGONSCAN_API_KEY = os.getenv('POLYGONSCAN_API_KEY')
response_matic_supply = requests.get('https://api.polygonscan.com/api?module=stats&action=maticsupply&apikey='+POLYGONSCAN_API_KEY)
print(response_matic_supply)
print(response_matic_supply.json())
matic_supply=response_matic_supply.json()
matic=matic_supply["result"]
print(matic_supply["result"])

#format matic with commas
my_int=  int(matic)*10**(-18)
print(type(my_int))
matic_formatted = f'{my_int:,}'
print(matic_formatted)

#colours
colors = {
    'black' : '#1A1B25',
    'red' : '#F8C271E',
    'white' : '#EFE9E7',
    'background' : '#333333',
    'text' : '#FFFFFF'
}


# Build the components
header_component = html.H1("PEPETH : A Polygon Block Explorer", className = "text-center p-2", style = {'color': '#EFE9E7'}),
under_header_component = html.H5("Check out the latest stats", className = "text-center p-2", style = {'color': '#EFE9E7'}),


# Graphs
token = html.Div(token_value_over_time(365), style={'backgroundColor' : colors['background']}),
size = size_graph(SIZE, 'lines'),
time = time_graph(SIZE, 'lines'),
#transactions=transactions_graph(SIZE,"lines")

        # time_graph(SIZE, 'bar'),
block_n = html.Span(block_number(), className="justify-content-center"),
token_val = html.Span(token_value(), className="text-center d-flex justify-content-center"),
# total_supply = total_supply(),
# market_cap = market_cap(),

#navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("How it works", href="works.html"),
                dbc.DropdownMenuItem("Polygon stats", href="#"),
                dbc.DropdownMenuItem("Other crypto stats", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Explore",
        ),
    ],
    brand="PEPETH",
    brand_href="#",
    color="dark",
    dark=True,
)

# Jumbotron
jumbotron = html.Div(
    dbc.Container(
        [
    
            html.H1("PEPETH", className="display-2 text-center"),
            html.P(
                "A POLYGON BLOCK EXPLORER",
                className="lead text-center",
            ),
            html.Hr(className="my-2 text-center"),
            html.P(
                "The place to find all Polygon statistics",
                className="text-center"
            ),
            html.P(
                dbc.Button("Learn more", color="primary"), className="lead text-center text-center"
            ),
        
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)




# Design the layout
app.layout = html.Div([

dbc.Row(navbar),

dbc.Container([
    
        jumbotron,
         

            dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie( width="67%", height="67%")),
                dbc.CardBody([
                    html.H5('Token value in $'),
                     html.Br(),
                    html.H4(token_val),
                ], style={'textAlign':'center'})
            ]),
        ], width=4, 
                className='mt-4 mb-4'),
        
                dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie( width="67%", height="67%")),
                dbc.CardBody([
                    html.H5('Current block'),
                     html.Br(),
                    html.H4(block_n),
                ], style={'textAlign':'center'})
            ]),
        ], width=4, 
                className='mt-4 mb-4'),
                
                             dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie( width="67%", height="67%")),
                dbc.CardBody([
                    html.H5('Matic supply (MATIC)'),
                    html.Br(),
                    html.H4(matic_formatted),
                ], style={'textAlign':'center'})
            ]),
        ], width=4, 
                className='mt-4 mb-4'),
                
        ]),

            dbc.Row(
            [dbc.Col(
                token
                ), 
            
            dbc.Col(
                size
                ) 
            ]
        ),
        
        # dbc.Row(
        # [dbc.Col(), dbc.Col()]
        # ),
    html.Div("PEPETH 2022", className="fixed-bottom bg-primary text-white text-center")
    
     ]


)
])




# Run the app
if __name__ == "__main__":
    app.run_server(port=8508,debug=True)
