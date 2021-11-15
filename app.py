#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 13:20:01 2021

@author: iyasueibed
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv('Correlation_DB_DT_Combined.csv')
df = df.dropna()
df['text'] = df['Algorithm'] + ', ' + df['Satellite'] + ' for ' + df['Station Name'] + ' Station' + ', \
             R = ' + df['Correlation Coefficient'].round(2).astype(str)

available_algorithm = df['Algorithm'].unique()
available_satellite = df['Satellite'].unique()
available_combination = df['Temporal Spatial Combination'].unique()

paper_link = "https://doi.org/10.3390/rs13122316"
guthub_link = "https://github.com/EngIyasu/AERONET-MODIS-AOD-Comparison-Dash-App"
linkedin_link = "https://www.linkedin.com/in/iyasu-g-eibedingil-01093a92"
datasource_link = "https://doi.org/10.17632/9v6pwjzxg6.1 "

colors = {
    'background': '#000000',
    'text': '#7FDBFF',
    'dropdown_title': '#ffffff'
}

href = "https://doi.org/10.3390/rs13122316"

#dcc.Link(html.A('Go to page 2 without refreshing!'), href="/page-2", style={'color': 'blue', 'text-decoration': 'none'}),
 
app.layout = html.Div(style={'backgroundColor': colors['background']}, className='row', children=[
    dcc.Link(html.H3('Comparison of Aerosol Optical Depth from MODIS Product Collection 6.1 and AERONET in the Western United States'), \
             href=paper_link,target='_blank', \
            style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div([
        
        html.Div([
            html.Label(['Algorithm Type:'], style={'font-weight': 'bold', "text-align": "center",'color': colors['dropdown_title']}),
            dcc.Dropdown(
                id='algorithm-column',
                options=[{'label': i, 'value': i} for i in available_algorithm],
                value='Deep Blue'
            )
        ], style=dict(width='33.33%')),
        
        html.Div([
            html.Label(['Satelllite Type:'], style={'font-weight': 'bold', "text-align": "center",'color': colors['dropdown_title']}),
            dcc.Dropdown(
                id='satellite-column',
                options=[{'label': i, 'value': i} for i in available_satellite],
                value='Aqua'
            )
        ], style=dict(width='33.33%')),
   
        html.Div([
            html.Label(['Temporal & Spatial Aggregation Domain:'], style={'font-weight': 'bold', "text-align": "center",'color': colors['dropdown_title']}),
            dcc.Dropdown(
                id='combination-column',
                options=[{'label': i, 'value': i} for i in available_combination],
                value='Nearest - Nearest'
            )
        ], style=dict(width='33.33%')),
    ],style=dict(display='flex')),

    dcc.Graph(id='MODIS-AERONET-Correlation-Coefficient'),
    
    html.A('LinkedIn Account', href=linkedin_link, target='_blank'),
    html.A('Code on Github', href=guthub_link,target='_blank', style={"margin-left": "30px"}),
    html.A('Data Source', href=datasource_link,target='_blank', style={"margin-left": "30px"}),
    
    
]) 


@app.callback(
    Output('MODIS-AERONET-Correlation-Coefficient', 'figure'),
    Input('algorithm-column', 'value'),
    Input('satellite-column', 'value'),
    Input('combination-column', 'value'))

def update_graph(algorithm_column_name,satellite_column_name, combination_column_name): 
    
    dff = df[(df['Algorithm'] == algorithm_column_name) & (df['Satellite'] == satellite_column_name) & \
             (df['Temporal Spatial Combination'] == combination_column_name)]
    
    fig = go.Figure(data=go.Scattergeo(
            lon = dff['Longitude'],
            lat = dff['Latitude'],
            text = dff['text'],
            mode = 'markers',
            marker = dict(
                size = 16,
                opacity = 0.7,
                reversescale = False,
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = 'jet',
                color = dff['Correlation Coefficient'],
                colorbar = dict(
                    titleside = "right",
                    outlinecolor = "rgba(68, 68, 68, 0)",
                    ticks = "outside",
                    showticksuffix = "last",
                    xanchor="left",
                    x=0.75,
                    dtick = 0.1
                ),             
                cmin = 0,
                cmax = 1, 
                colorbar_title="Correlation <br> Coefficient (R)"
            )))
        
    fig.update_layout(
        margin=dict(l=10, r=0, t=20, b=10,pad=0),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        autosize=False,
        height=700,
        width=1600,
        geo = dict(
            scope='north america',
            projection = dict(
                type = 'conic conformal',
                rotation_lon = -100
            ),
            showland = True,
            landcolor="rgb(212, 212, 212)",
            subunitcolor = "RebeccaPurple",
            countrycolor="RebeccaPurple",
            countrywidth = 1,
            subunitwidth = 0.3,
            showlakes = True,
            lakecolor = "rgb(255, 255, 255)",
            showsubunits = True,
            showcountries = True,
            resolution = 50,
            lonaxis = dict(
                showgrid = True,
                gridwidth = 0.5,
                range= [ -122.0, -92.0 ],
                dtick = 5
            ),
            lataxis = dict(
                showgrid = True,
                gridwidth = 0.5,
                range= [ 26.5, 50.0 ],
                dtick = 5
            )
        ),
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)