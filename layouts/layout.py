import dash_core_components as dcc
import dash_html_components as html
from . import layout_introduction
from . import layout_simulation
from . import layout_point_process_introduction

def generate_layout():
    return html.Div([
        # title
        generate_title(),

        # empty line
        html.Br(),

        # the core functionality area
        html.Div([

            # margins
            generate_margin(),

            # tabs and the figures
            html.Div([generate_tab()
                      ], className='col-sm-10'),
            generate_margin()

        ],
            className='row'
        )
    ],className='maincontainer'
    )


def generate_title():
    "return a Div containing the title"

    return html.Div([

        html.Div([], className='col-sm-2'),  # Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H1(children='Coral Sampling Tool',
                    style={'textAlign': 'center'},
                    id='title'
                    )],
            className='col-sm-8',
            style={'padding-top': '1%'}
        ),



        html.Div([], className='col-sm-2')
    ],
        className='row'
    )



def generate_margin():
    return html.Div([], className='col-sm-1')

def generate_tab():
    "return a Div containing the tabs of survey graph, simulation graph, and power calculation result"

    return dcc.Tabs([

        dcc.Tab(label='Introduction', children=[layout_introduction.generate_brief_introduction_tab()]),
        # dcc.Tab(label='Survey', children=[
        #     generate_survey_graph()
        # ]),


        dcc.Tab(label='Map Corals', children=[layout_point_process_introduction.generate_point_process_introduction()]),

        dcc.Tab(label='Simulation', children=[
            layout_simulation.generate_simulation_tab()
        ]),

        dcc.Tab(label='Background Information', children=[layout_introduction.generate_introduction_tab()])

    ], id='main_tab')

