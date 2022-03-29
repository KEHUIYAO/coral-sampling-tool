from dash.dependencies import Input, Output, State
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app


# instruction to let the user select a region on the map
@app.callback(Output('text_select_region', 'style'),
              Input('button_select_region', 'n_clicks'))
def show_instruction(n):
    if n > 0:
        return {"display": "block", "color": "red"}
    return {"display": "none"}

# once there is a region selected, the instruction and the selectbox to carry on the next step will pop out
@app.callback(
    Output('text_dropdown_select_process', 'style'),
    Output('dropdown_select_process', 'style'),
    Input('store_prop_cover_estimation', 'data'),
    Input('graph_data_visualization', 'selectedData'))
def display_selected_data(prop_cover_estimation, selected_data):
    if selected_data:
        print('hello')
        print(selected_data)
        print(prop_cover_estimation)
        return {"display": "block", "color": "red"}, {"display": "block"}
    else:
        return {"display": "none"}, {"display": "none"}