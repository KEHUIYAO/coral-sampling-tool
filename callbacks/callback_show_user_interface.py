import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from dash.dependencies import Input, Output


# once a point process is selected, show the user interface
# instruction text
@app.callback(Output('text_input_process_parameters', 'style'),
              Input('dropdown_select_process', 'value'),
              prevent_initial_call=True
              )
def show(process):
    return {'display': 'block', 'color': 'red'}


# show simulation button and power calculation buttons
@app.callback(Output('show_two_buttons', 'style'),
              Input('dropdown_select_process', 'value'),
              prevent_initial_call=True
              )
def show(process):
    return {'display': 'block'}


# @app.callback(
#     Output('text_input_process_parameters', 'style'),
#     Output('button_start_simulation', 'style'),
#     Output('text_power_calculation_instruction', 'style'),
#     Output('input_power_calculation_repeatitions', 'style'),
#     Output('button_power_calculation', 'style'),
#     Input('dropdown_select_process', 'value')
# )
# def show_instructions_after_a_point_process_is_selected(process):
#     if process == 0:
#         return {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}
#     else:
#         return {'display':'block'}, {'display':'block'}, {'display':'block'}, {'display':'block'},  {'display':'block'}

# user's input
@app.callback(
    Output("input_disease_prevalence_container", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    return {'display': 'block'}


# @app.callback(
#     Output("input_coral_size", "style"),
#     Input("dropdown_select_process","value")
# )
# def show(process):
#     if process == 0:
#         return {'display':'none'}
#     else:
#         return {'display':'block'}
#
# @app.callback(
#     Output("input_coral_size_sd", "style"),
#     Input("dropdown_select_process","value")
# )
# def show(process):
#     if process == 0:
#         return {'display':'none'}
#     else:
#         return {'display':'block'}


@app.callback(
    Output("input_n_toolkits_container", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    return {'display': 'block'}


@app.callback(
    Output("show_input_fun_lambda", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    if process == 2:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output("show_input_parent_prop", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    if process == 3:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output("show_input_parent_range", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    if process == 3:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# @app.callback(
#     Output("input_strauss_beta", "style"),
#     Input("dropdown_select_process", "value")
# )
# def show(process):
#     if process == 4:
#         return {'display': 'block'}
#     else:
#         return {'display': 'none'}
#
#
# @app.callback(
#     Output("input_strauss_gamma", "style"),
#     Input("dropdown_select_process", "value")
# )
# def show(process):
#     if process == 4:
#         return {'display': 'block'}
#     else:
#         return {'display': 'none'}

#
# @app.callback(
#     Output("input_strauss_R", "style"),
#     Input("dropdown_select_process", "value")
# )
# def show(process):
#     if process == 4:
#         return {'display': 'block'}
#     else:
#         return {'display': 'none'}
#
#

@app.callback(
    Output("input_transect_length", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    return {'display': 'block'}



@app.callback(
    Output("input_transect_width", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    return {'display': 'block'}



@app.callback(
    Output("line_intercept_ratio", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    return {'display': 'block'}



@app.callback(
    Output("coral_size_input", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    return {'display': 'block'}

@app.callback(
    Output("coral_size_std_input", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    return {'display': 'block'}

@app.callback(
    Output("prop_cover_input", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    if process == 2:
        return {'display':'none'}
    return {'display': 'block'}

@app.callback(
    Output("number_of_replications_input", "style"),
    Input("dropdown_select_process", "value"),
    prevent_initial_call=True
)
def show(process):
    return {'display': 'block'}