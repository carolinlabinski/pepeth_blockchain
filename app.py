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

response_gas_price= requests.get('https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey='+POLYGONSCAN_API_KEY)

gas_price_json=response_gas_price.json()
print(gas_price_json)
print(type(gas_price_json))
print(gas_price_json.keys())
gas_prices=gas_price_json["result"]
print(gas_prices)
propose_gas_price=gas_prices["ProposeGasPrice"]
safe_gas_price=gas_prices["SafeGasPrice"]
usd_price=gas_prices["UsdPrice"]
fast_gas_price=gas_prices["FastGasPrice"]
last_block=gas_prices["LastBlock"]
fast_gas_price=gas_prices["FastGasPrice"]
gas_used_ratio=gas_prices["gasUsedRatio"]
suggest_base_fee=gas_prices["suggestBaseFee"]

usd_price_float=float(usd_price)
print(propose_gas_price)
print(safe_gas_price)
print(usd_price)
print(fast_gas_price)
print(gas_used_ratio)
print("type usd dollar")
print(type(usd_price_float))
print(type(usd_price))

#matic market cap
#matic_market_cap=usd_price_float*float(matic_formatted)
matic_market_cap=usd_price_float*my_int
print("matic_market_cap")
print(usd_price)
print(matic_formatted)
print(my_int)
print(matic_market_cap)

#Get a list of 'Normal' Transactions/number of transactions By Address
#Returns the list of transactions performed by an address, with optional pagination

response_transaction_list= requests.get('https://api.polygonscan.com/api?module=account&action=txlist&address=0x0000000000000000000000000000000000001010&startblock=0&endblock=99999999&page=10&offset=20&sort=asc&apikey='+POLYGONSCAN_API_KEY)

transaction_list_json=response_transaction_list.json()
print(transaction_list_json)
print(type(transaction_list_json))
print(transaction_list_json.keys())
transactions=transaction_list_json["result"]
print(transactions)
print(type(transactions))


df=pd.DataFrame(transaction_list_json["result"]).sort_values(by=['timeStamp'], ascending=False)
df["timeStamp"]=pd.to_datetime(df["timeStamp"],unit="s")
print(df["timeStamp"])
print(df)
print(df["timeStamp"])
print(df["gasUsed"])

x_time=df["timeStamp"]
y_gasused=df["gasUsed"]


#fig = px.bar(df, x=df["timeStamp"], y=df["gasUsed"], title='Polygon Transactions')
#fig.show()

#polgygon_barchart=px.bar(df, x=df["timeStamp"], y=df["gasUsed"], title='Polygon Transactions')





#api alphavantage
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
url = "https://alpha-vantage.p.rapidapi.com/query"

querystring = {"market":"USD","function":"DIGITAL_CURRENCY_MONTHLY","symbol":"MATIC"}

headers = {
    "X-RapidAPI-Key": ALPHA_VANTAGE_API_KEY,
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
response_json=response.json()
print(response_json)
print(response_json.keys())
df=pd.DataFrame(response_json["Time Series (Digital Currency Monthly)"])
print(df)
df_new=df.transpose()
print(df_new)

print("print index")
idx = df_new.index
print(idx)
print(type(idx))

# iterating the columns
print("column names")
for col in df_new.columns:
    print(col)

#graph candlestick
#fig = go.Figure(data=[go.Candlestick(x=df_new.iloc[:, 0],
fig = go.Figure(data=[go.Candlestick(x=idx,
               open=df_new['1a. open (USD)'],
               high=df_new['2a. high (USD)'],
              low=df_new['3a. low (USD)'],
              close=df_new['4a. close (USD)'])])

fig.update_layout(
    title="Monthly MATIC candlestick chart")

# Daily MATIC query
url = "https://alpha-vantage.p.rapidapi.com/query"

querystring_daily = {"function":"DIGITAL_CURRENCY_DAILY","symbol":"MATIC","market":"EUR"}

headers = {
    "X-RapidAPI-Key": ALPHA_VANTAGE_API_KEY,
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

response_daily = requests.request("GET", url, headers=headers, params=querystring_daily)
response_json_daily=response_daily.json()
# print(response_json)
# print(response_json.keys())
df_daily=pd.DataFrame(response_json_daily["Time Series (Digital Currency Daily)"])
print(df_daily)
print(type(df_daily["2022-11-17"]))
df_newest=df_daily.transpose()
print(df_newest)


#graph candlestick
idx_daily = df_newest.index
print("check daily index")
print(idx_daily)
print(df_newest)
fig_daily_candlestick = go.Figure(data=[go.Candlestick(x=idx_daily,
               open=df_newest['1a. open (EUR)'],
               high=df_newest['2a. high (EUR)'],
              low=df_newest['3a. low (EUR)'],
              close=df_newest['4a. close (EUR)'])])

fig_daily_candlestick.update_layout(
    title="Daily MATIC candlestick chart")             




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
                    html.H5('Matic Market Cap in $'),
                     html.Br(),
                    html.H4(matic_market_cap),
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

                    dbc.Row([
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
                    html.H5('Safe Gas Price'),
                     html.Br(),
                    html.H4(safe_gas_price),
                ], style={'textAlign':'center'})
            ]),
        ], width=4, 
                className='mt-4 mb-4'),
                
                             dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie( width="67%", height="67%")),
                dbc.CardBody([
                    html.H5('Proposed Gas Price'),
                    html.Br(),
                    html.H4(propose_gas_price),
                ], style={'textAlign':'center'})
            ]),
        ], width=4, 
                className='mt-4 mb-4'),
                
        ]),
        dcc.Graph(figure=fig),
        dcc.Graph(figure=fig_daily_candlestick),
        
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
