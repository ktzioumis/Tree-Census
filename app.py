import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df_2015=pd.read_csv('new_york_tree_census_2015.csv')
#tree_name='pine'

app.layout = html.Div(children=[
    html.H1(children='NYC Tree Mapper'),

    html.Div(children='''
        Using Dash to map the location of different types of trees across New York City.
    '''),
html.Label('Map This Tree Type:'),
    dcc.Input(id='text_in',value='pine', type='text'),

    
    dcc.Graph(
        id='tree_map',
        figure={'layout': go.Layout(height=600,mapbox_style="carto-positron",
                  mapbox_zoom=9, mapbox_center = {"lat": 40.7, "lon": -73.86},margin={"r":0,"t":30,"l":0,"b":0})}
        
    )])

@app.callback(
    Output(component_id='tree_map',component_property='figure'),
    [Input('text_in','value')])
def update_tree(tree_name):
    data=[]
    for t in df_2015.dropna().loc[df_2015.dropna()['spc_common'].str.contains(tree_name)]['spc_common'].value_counts().index:
        data.append(go.Scattermapbox(lat=df_2015.dropna().loc[df_2015.dropna()['spc_common']==t]['latitude'],
                               lon=df_2015.dropna().loc[df_2015.dropna()['spc_common']==t]['longitude'],
                               mode='markers',
                                 name=t,
                              marker=go.scattermapbox.Marker(size=5)
                      ))
    return {
            'data': data,
            'layout': go.Layout(height=600, mapbox_style="carto-positron",
                  mapbox_zoom=9, mapbox_center = {"lat": 40.7, "lon": -73.86},margin={"r":0,"t":30,"l":0,"b":0})
        }
     
     
if __name__ == '__main__':
    app.run_server(debug=True)