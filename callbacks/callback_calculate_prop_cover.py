from dash.dependencies import Input, Output, State
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utilities
from main import app
import pandas as pd


# once there is a region selected, calculate the estimated prop_cover
# after calculating the prop cover, store it into the hidden div
@app.callback(Output('prop_cover_estimate', 'style'),
              Output('prop_cover_estimate', 'children'),
              Output('store_prop_cover_estimation', 'data'),
              Input('data', 'data'),
              Input('graph_data_visualization', 'selectedData'))
def show_prop_cover_estimate(data, selected_data):
    data = pd.read_json(data, orient='split')

    if not selected_data:
        return {"display": "none"}, [], 0
    prop_cover = utilities.estimate_density_based_on_selected_sites(selected_data, data)


    if len(selected_data['points']) == 0:

        # too far from the historical sites
        if prop_cover == 0.03:
            text = 'The selected region is too far from the historical sites, just set the proportion cover to be the default value 0.03.'

        # estimate using k-nearest sites
        else:
            text = 'Based on the selected region, there are no historical sites selected, we will use 10 nearest historical sites to estimate the proportion cover. The estimated proportion cover in this region is %.4f.' % prop_cover

    else:
        num_sites = len(selected_data['points'])
        text = 'Based on the selected region, there are %d historical sites. The estimated proportion cover in this region is %.4f.' %(num_sites, prop_cover)



    return {"display": "none"}, text, prop_cover


