import dash_table
from dash.dependencies import Input, Output, State
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from coralsim import utility
import utilities
from main import app
import dash_html_components as html




# core function to perform power calculation
@app.callback(
    Output('text_power_calculation', 'children'),
    Output('text_power_calculation', 'style'),
    Output('intro_power_calculation', 'style'),

    Input('button_power_calculation', 'n_clicks'),
    Input('store_prop_cover_estimation', 'data'),
    State('num_of_replications', 'value'),
    State('graph_data_visualization', 'selectedData'),
    State('dropdown_select_process', 'value'),
    State('input_disease_prevalence', 'value'),
    State('input_n_toolkits', 'value'),
    State('input_fun_lambda', 'value'),
    State('input_parent_prop', 'value'),
    State('input_parent_range', 'value'),
    State('input_strauss_beta', 'value'),
    State('input_strauss_gamma', 'value'),
    State('input_strauss_R', 'value'),
    State('dcc_input_transect_length', 'value'),
    State('dcc_input_transect_width', 'value'),
    State('dcc_line_intercept_ratio', 'value'),
    State('coral_size', 'value'),
    State('coral_size_std', 'value'),
    State('prop_cover', 'value')
)
def power_calculation(n_clicks, prop_estimation, n_rep, selected_data, dropdown_select_process,
                      disease_prevalence, n_toolkits, fun_lambda, parent_prop,
                      parent_range, strauss_beta, strauss_gamma, strauss_R,
                      transect_length, transect_width, line_intercept_ratio,
                      coral_size, coral_size_std, prop_cover
                      ):
    if n_clicks == 0:
        return '', {'display': 'none'}, {'display':'block'}
    else:

        # estimate the prop_cover if prop cover is not given
        if prop_cover == 0:
            prop_cover = prop_estimation

        # generate the setting
        setting, _, _ = utilities.generate_setting(dropdown_select_process, prop_cover,
                                      disease_prevalence, n_toolkits, fun_lambda, parent_prop,
                                      parent_range, strauss_beta, strauss_gamma, strauss_R, selected_data,
                                      transect_length, transect_width, line_intercept_ratio,
                                      coral_size, coral_size_std
                                      )

    # power calculation by repeated simulation
    # single toolkit
    n_toolkits = [n_toolkits]
    # multiple toolkits
    #n_toolkits = [1, 2, 3, 4, 5]


    df = utility.power_comparison_using_different_number_of_toolkits_2(setting, n_toolkits, n_rep, write_to_csv=False,
                                                                return_table=True)  # power of prop cover estimation



    res_table = dash_table.DataTable(
        id='table',

        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )

    # text_power_calculation = "Using %d toolkits under %d reptitions, the power is %f." % (n_toolkits, n_rep, res[0])
    # return text_power_calculation, {'display':'block'}

    return res_table, {'display': 'block'}, {'display': 'block'}

@app.callback(
    Output('text_number_of_replications', 'children'),
    Input('button_power_calculation', 'n_clicks'),
    State('num_of_replications', 'value'),
    prevent_initial_call=True
)
def update(n_clicks, n_rep):
    if n_clicks > 0:
        text = 'After %d replications, the results are as follows:'%n_rep
        return html.Div(text)
