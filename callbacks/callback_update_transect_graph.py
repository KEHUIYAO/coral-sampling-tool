import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dash.dependencies import Input, Output, State
from dash import callback_context
import utilities
from main import app
import dash_html_components as html
import pyproj
import dash_bootstrap_components as dbc
import pandas as pd


# core function to update transect graph and all the text result
@app.callback(
    Output('graph_simulation_visualization', 'figure'),
    Output('line_intercept_estimation', 'children'),
    Output('graph_simulation_visualization', 'style'),
    Output('line_intercept_estimation', 'style'),
    Output('transect_location', 'children'),
    Output('transect_location', 'style'),
    # Output('sampling_plans_text','data'),
    Output('sampling_plans_table', 'data'),
    Output('show_download_button', 'style'),
    Input('button_start_simulation', 'n_clicks'),
    State('store_prop_cover_estimation', 'data'),
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
    State('prop_cover', 'value'),
    prevent_initial_call=True
)
def update_simulation_graph(n_clicks, prop_cover_estimation, selected_data, dropdown_select_process,
                            disease_prevalence, n_toolkits, fun_lambda, parent_prop,
                            parent_range, strauss_beta, strauss_gamma, strauss_R,
                            transect_length, transect_width, line_intercept_ratio,
                            coral_size, coral_size_std, prop_cover,

                            ):
    # if the prop cover is not given, estimate the prop_cover based on the historical data
    if prop_cover == 0:
        prop_cover = prop_cover_estimation

    # generate the setting
    setting, area, p = utilities.generate_setting(dropdown_select_process, prop_cover,
                                     disease_prevalence, n_toolkits, fun_lambda, parent_prop,
                                     parent_range, strauss_beta, strauss_gamma, strauss_R, selected_data,
                                     transect_length, transect_width, line_intercept_ratio,
                                     coral_size, coral_size_std
                                     )

    # simulate once
    setting.efficient_simulate()

    # estimate the prop cover based on the line intercept method
    prop_cover_mean, prop_cover_sd, CI = setting.estimate_prop_cover()
    # prop_cover_list = []
    # for i in range(10):
    #     setting.efficient_simulate()
    #     prop_cover_list.append(setting.estimate_prop_cover())
    #
    # prop_cover_mean = np.mean(prop_cover_list)
    # prop_cover_sd = np.std(prop_cover_list)
    # CI = [prop_cover_mean - 1.96 * prop_cover_sd, prop_cover_mean + 1.96 * prop_cover_sd]


    # plot for one simulation
    fig = setting.plot_with_plotly()

    # estimate the prevalence based on one setting
    prevalence, sd_prevalence, (ci_lower, ci_upper) = setting.estimate_prevalence()

    text = "Proportion cover based on the line intercept method is: %.4f, with a standard deviation equals %.4f. The credible interval is (%.4f, %.4f). Prevalence estimation is: %.4f, with standard deviation equals %.4f. The credible interval is (%.4f, %.4f)."%(prop_cover_mean, prop_cover_sd, CI[0], CI[1], prevalence, sd_prevalence, ci_lower, ci_upper)


    # reproject the transect center to long and lat
    placement = setting.sampling_planner.placement
    print(placement)


    text_placement = ''

    df = []

    for i in placement:
        x, y, rotation = i[0], i[1], i[2]
        lon, lat = p(x, y, inverse=True)
        temp_text = 'Place one transect with a start point at lon %.6f, lat %.6f and then run the transect at a compass bearing of %.2f .'%(lon, lat, 360-rotation)

        df.append([lat, lon, 360-rotation])

        text_placement += temp_text

    df = pd.DataFrame(df,
                      columns=['Latitude', 'Longitude', 'Compass Bearing'])

    df = df.to_dict('records')

    return fig, text, {'display':'block'},  {'display':'block'}, text_placement, {'display':'block'}, df, {'display':'block'}

@app.callback(
    Output('selected_region_information', 'children'),
    Output('selected_region_information', 'style'),
    Input('button_start_simulation', 'n_clicks'),
    State('graph_data_visualization', 'selectedData'),
    prevent_initial_call=True

)
def update_selected_region_information(n_clicks, selected_data):
    warnings = ''

    if 'range' in selected_data.keys():
        mapbox = selected_data['range']['mapbox']
        longitude = [mapbox[0][0], mapbox[1][0]]
        latitude = [mapbox[0][1], mapbox[1][1]]
        p = pyproj.Proj('epsg:2337', preserve_units=False)
        left_up = p(*mapbox[0])
        right_down = p(*mapbox[1])
        area = abs(right_down[0] - left_up[0]) * abs(right_down[1] - left_up[1])

        # transform to square kilometers
        area_square_kilo_meters = area / (1000 * 1000)

        warnings = 'The selected area is %.2f square kilometers.' %area_square_kilo_meters

        # if area < 10000 or area > 40000:
        #     if area < 10000:
        #         warnings = "The selected region is too small! The selected area is %.2f square kilometers. (The allowable size of the selected region is from 0.1 to 0.4 square kilometers). We've automatically select a region containing your selected region and project it onto a 2D space using " %area_square_kilo_meters
        #
        #     else:
        #         warnings = "The selected region is too large! The selected area is %.2f square kilometers. (The allowable size of the selected region is from 0.1 to 0.4 square kilometers). We've automatically select a region within your selected region and project it onto a 2D space using " %area_square_kilo_meters


        text = "The longitude of the survey region you've selected is from %.2f to %.2f. The latitude is from %.2f to %.2f."%(longitude[0], longitude[1], latitude[1], latitude[0])

    else:
          warnings = 'Use a constant 100x100 square for simulation.'
          text = 'You are using lasso select tool, try to use box select tool to obtain the longitude and latitude of the selected region.'

    epsg = html.Span('epsg:2337.', id='epsg', className='highlight')
    epsg_tooltip = dbc.Tooltip('+proj=tmerc +lat_0=0 +lon_0=135 +k=1 +x_0=23500000 +y_0=0 +a=6378140 +b=6356755.288157528 +units=m +no_defs', target='epsg')


    # return [text, ' ', warnings, epsg, epsg_tooltip], {'display':'block'}
    return [warnings, ' ', text, epsg, epsg_tooltip], {'display':'block'}

# automatically switch tab after pressing the simulation button
@app.callback(
    Output('inline-tab','value'),
    Input('button_start_simulation', 'n_clicks'),
    Input('button_power_calculation', 'n_clicks'),
    prevent_initial_call=True
)
def change_tab(b1, b2):
    triggered_id = callback_context.triggered[0]['prop_id']
    if 'button_start_simulation.n_clicks' == triggered_id:
        return 'tab-2'
    elif 'button_power_calculation.n_clicks' == triggered_id:
        return 'tab-3'


# download the result
# @app.callback(Output("download", "data"),
#               Input("button_download", "n_clicks"),
#               State('sampling_plans_text', 'data'),
#               prevent_initial_call=True
#               )
# def func(n_clicks, text):
#     return dict(content=text, filename="result.txt")


# download the result as a table
@app.callback(Output('table_to_download', 'data'),
              Input('sampling_plans_table', 'data'),
              prevent_initial_call=True
              )
def func(df):
    return df
