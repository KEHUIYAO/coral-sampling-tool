import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import shapely.geometry as sg
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from coralsim import CoralGenerator
from dash.exceptions import PreventUpdate

# update homogeneous poisson process
@app.callback(
    Output('homogeneous_poisson_process', 'figure'),
    Output('text_homogeneous_poisson_process', 'children'),
    Output('homogeneous_poisson_process', 'style'),
    Input('intro_button_1', 'n_clicks'),
    State('intro_lambda', 'value'),
    State('intro_coral_size', 'value'),
    State('intro_coral_size_std', 'value'),
    State('intro_prevalence_rate', 'value'),
    State('intro_tab', 'value'),
    prevent_initial_call=True

)
def update_visualization(n_clicks, intensity, coral_size, coral_size_std, disease_rate, which_process):
    if which_process == 'tab-1':
        area = sg.Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])
        coral_generator = CoralGenerator.CoralGenerator(area)
        #coral_size = np.mean(np.array([109, 72, 42, 50])) / 100 ** 2
        #coral_size_std = 0.001
        coral_generator.generate_coral_from_homogeneous_poisson_process(disease_rate, coral_size, coral_size_std, intensity)

        fig = coral_generator.plot_with_plotly(alpha=0.1)
        fig.update_layout(
            xaxis_title="meters",
            yaxis_title="meters"
        )
        fig.update_layout(height=600, width=600)
        corals_per_square_meter = len(coral_generator.corals) / (4 * 4)
        text = "The number of corals per square meter is %.4f." % corals_per_square_meter

        return fig, text, {'display':'block'}
    else:
        raise PreventUpdate



# update inhomogeneous poisson process
@app.callback(
    Output('inhomogeneous_poisson_process', 'figure'),
    Output('text_inhomogeneous_poisson_process', 'children'),
    Output('inhomogeneous_poisson_process', 'style'),
    Input('intro_button_1', 'n_clicks'),
    State('intro_fun_lambda', 'value'),
    State('intro_coral_size_inhomogeneous', 'value'),
    State('intro_coral_size_std_inhomogeneous', 'value'),
    State('intro_prevalence_rate_inhomogeneous', 'value'),
    State('intro_tab', 'value'),
    prevent_initial_call=True

)
def update_visualization(n_clicks, fun_lambda, coral_size, coral_size_std, disease_rate, which_process):
    if which_process == 'tab-2':
        fun_lambda = eval('lambda x,y: ' + fun_lambda)
        area = sg.Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])
        coral_generator = CoralGenerator.CoralGenerator(area)
        coral_generator.generate_coral_from_inhomogeneous_poisson_process(disease_rate, coral_size, coral_size_std, fun_lambda)

        fig = coral_generator.plot_with_plotly(alpha=0.1)
        fig.update_layout(height=600, width=600)

        corals_per_square_meter = len(coral_generator.corals) / (4 * 4)

        text = "The number of corals per square meter is %.4f." % corals_per_square_meter


        return fig, text, {'display':'block'}

    else:
        raise PreventUpdate



# update poisson clustering process
@app.callback(
    Output('poisson_clustering_process', 'figure'),
    Output('text_possion_clustering_process', 'children'),
    Output('poisson_clustering_process', 'style'),
    Input('intro_button_1', 'n_clicks'),
    State('intro_lambda_2', 'value'),
    State('intro_coral_size_poisson', 'value'),
    State('intro_coral_size_std_poisson', 'value'),
    State('intro_parent_intensity', 'value'),
    State('intro_offspring_range', 'value'),
    State('intro_prevalence_rate_3', 'value'),
    State('intro_tab', 'value'),
    prevent_initial_call=True

)
def update_visualization(n_clicks, lambda_intensity, coral_size, coral_size_std, parent_intensity, offspring_range, disease_rate, which_process):
    if which_process == 'tab-3':
        area = sg.Polygon([(0, 0), (0, 4), (4, 4), (4, 0)])
        coral_generator = CoralGenerator.CoralGenerator(area)

        coral_generator.generate_coral_from_poisson_cluster_process(disease_rate, coral_size, coral_size_std, lambda_intensity, parent_intensity, offspring_range)

        fig = coral_generator.plot_with_plotly(alpha=0.6)
        fig.update_layout(height=600, width=600)

        corals_per_square_meter = len(coral_generator.corals) / (4 * 4)

        text = "The number of corals per square meter is %.4f."%corals_per_square_meter

        return fig, text, {'display':'block'}
    else:
        raise PreventUpdate


# port the parameters to real coral simulation
@app.callback(
    Output('coral_size', 'value'),
    Output('coral_size_std', 'value'),
    Output('prop_cover', 'value'),
    Output('input_disease_prevalence', 'value'),
    Output('input_fun_lambda', 'value'),
    Output('input_parent_prop', 'value'),
    Output('input_parent_range', 'value'),
    Input('intro_port', 'n_clicks'),
    State('intro_coral_size', 'value'),
    State('intro_coral_size_std', 'value'),
    State('intro_lambda', 'value'),
    State('intro_prevalence_rate', 'value'),
    State('intro_fun_lambda', 'value'),
    State('intro_coral_size_inhomogeneous', 'value'),
    State('intro_coral_size_std_inhomogeneous', 'value'),
    State('intro_prevalence_rate_inhomogeneous', 'value'),
    State('intro_lambda_2', 'value'),
    State('intro_coral_size_poisson', 'value'),
    State('intro_coral_size_std_poisson', 'value'),
    State('intro_parent_intensity', 'value'),
    State('intro_offspring_range', 'value'),
    State('intro_prevalence_rate_3', 'value'),
    State('intro_tab', 'value'),
    prevent_initial_call=True

)
def port_parameters(n_clicks,coral_size_homo, coral_size_std_homo, prop_cover_homo, disease_rate_homo, fun_lambda, coral_size_inhomo, coral_size_std_inhomo, disease_rate_inhomo, prop_cover_cluster, coral_size_cluster, coral_size_std_cluster, parent_prop, parent_range, disease_rate_cluster, which_process):
    if which_process == 'tab-1':
        return coral_size_homo, coral_size_std_homo, prop_cover_homo, disease_rate_homo, "1000 * np.exp(-(((x - 50) / 50) ** 2 + ((y - 50) / 50) ** 2) / 0.5 ** 2)", 0.01, 5
    elif which_process == 'tab-2':
        return coral_size_inhomo, coral_size_std_inhomo, 0, disease_rate_cluster, fun_lambda, 0.01, 5
    elif which_process == 'tab-3':
        return coral_size_cluster, coral_size_std_cluster, prop_cover_cluster, disease_rate_cluster,  "1000 * np.exp(-(((x - 50) / 50) ** 2 + ((y - 50) / 50) ** 2) / 0.5 ** 2)", parent_prop, parent_range


# after clicking the port parameters button, switch to simulation tab
@app.callback(
    Output('main_tab', 'value'),
    Input('intro_port', 'n_clicks'),
    prevent_initial_call=True
)
def switch_to_simulation(n_clicks):
    return 'tab-3'