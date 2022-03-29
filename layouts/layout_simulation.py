import dash_core_components as dcc
import dash_html_components as html
from . import layout_simulation_procedure
from . import layout_simulation_survey
from . import layout_simulation_transect_visualization
from . import layout_simulation_power_calculation

def generate_simulation_tab():
    return html.Div([html.Br(),
        html.Div([layout_simulation_procedure.generate_simulation_procedure(),
                     generate_inline_tab()], className='row')])

def generate_inline_tab():
    inline_tab = dcc.Tabs([

        dcc.Tab(label='Survey', children=[layout_simulation_survey.generate_survey_graph()
                                                         ]),
        # dcc.Tab(label='Survey', children=[
        #     generate_survey_graph()
        # ]),
        dcc.Tab(label='Transect Visualization', children=[
            layout_simulation_transect_visualization.generate_transect_visualization()
        ]),
        dcc.Tab(label="Power Calculation", children=[
             layout_simulation_power_calculation.generate_power_calculation_result()])
    ], id='inline-tab')

    return html.Div(inline_tab, className='col-sm-7')


