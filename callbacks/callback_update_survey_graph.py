import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from main import data
from dash.dependencies import Input, Output, State
import plotly.express as px
import io
import base64
import pandas as pd
import html



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            data = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))



    except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
    #print(data)
    return data


# data cleaning with the uploaded data and store it in the hidden data div
@app.callback(Output('data', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified')
              )
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        if 'csv' not in list_of_names[0]:
            return html.Div(['There was an error processing this file.'])

        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        #print(len(children))
        print(children[0])
        return children[0].to_json(orient='split')
        #return children[0]
    else:
        # if no data is uploaded, use the built-in one
        return data.to_json(orient='split')




# function to update the range slider
@app.callback(
    Output('RangeSlider-Year', 'min'),
    Output('RangeSlider-Year', 'max'),
    Output('RangeSlider-Year', 'marks'),
    Output('RangeSlider-Year', 'value'),
    Input('data', 'data')
)
def generate_range_slider(data):
    data = pd.read_json(data, orient='split')
    return (data.Year.astype('int32').min(),
           data.Year.astype('int32').max(),
           {i: '{}'.format(i) for i in
               range(data.Year.astype('int32').min(),
                     data.Year.astype('int32').max() + 1)},
         [data.Year.astype('int32').min(), data.Year.astype('int32').max()])


# core function to update the survey graph
@app.callback(
    Output('graph_data_visualization', 'figure'),
    Input('RangeSlider-Year', 'value'),
    Input('data', 'data')
)
def update_graph_data_visualization(value, data):
    #print(data)
    data = pd.read_json(data, orient='split')
    data['Year'] = data['Year'].astype(str)  # convert year to be categorical
    start_year = value[0]
    end_year = value[1]
    selected_years = [str(i) for i in list(range(start_year, end_year + 1))]
    subdata = data[data.Year.isin(selected_years)]
    fig = px.scatter_mapbox(subdata, lat="Latitude", lon="Longitude", color="Year", hover_data=["Site"])
    fig.update_layout(mapbox_style='open-street-map', height=600)
    return fig


