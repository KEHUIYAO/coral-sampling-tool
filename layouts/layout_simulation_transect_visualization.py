import dash_core_components as dcc
import dash_table
import dash_html_components as html



def generate_transect_visualization():
    "main function to generate the transect visualization tab"
    return html.Div([
        html.Br(),
        generate_selected_region_info(),
                     generate_simulation_graph(),
                     generate_text_transect_placement(),
                     html.Br(),
                     generate_line_intercept_estimation(),
        html.Br(),
        generate_download_button()])

def generate_selected_region_info():
    "return a Div containing the information of the region selected by the user"
    return dcc.Loading(html.Div(id='selected_region_information',style={'display':'none'}
                    ))

def generate_simulation_graph():
    "return a Div containing the simulation graph"
    return dcc.Loading(dcc.Graph(id='graph_simulation_visualization', style={'display':'none'}))

def generate_text_transect_placement():
    "return the lon and lat of the center of each transect"
    return html.Div(id='transect_location', style={'display':'none'})

def generate_line_intercept_estimation():
    "return a Div containing the prop cover estimated by the line intercept method"
    estimation = dcc.Loading([html.Div(["Prop cover based on the line intercept method is:"],id = 'line_intercept_estimation',style={'display':'none'}
    )])
    return html.Div([estimation])

def generate_download_button():
    "return a download button, which can export the sampling plans"

    result_table = dash_table.DataTable(
        id='table_to_download',
        columns = [{"name": i, "id": i} for i in ['Latitude', 'Longitude', 'Compass Bearing']],
        data=None,
        export_format='csv'
    )

    return html.Div(
        html.Div(
            [html.Div(className='col-sm-2'),
             result_table,
             dcc.Store(id='sampling_plans_table'),
             html.Div(className='col-sm-2')], className='row'
        ),id='show_download_button',style={'display':'none'})


    # return html.Div(
    #     html.Div(
    #     [html.Div(className='col-sm-2'),
    #      html.Button("Download sampling plans", id="button_download",className='col-sm-8'),
    #     Download(id="download"),
    #     dcc.Store(id='sampling_plans_text'),
    #     html.Div(className='col-sm-2')], className='row'
    # ),id='show_download_button',style={'display':'none'})


