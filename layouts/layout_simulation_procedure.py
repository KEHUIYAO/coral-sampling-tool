import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def generate_simulation_procedure():
    return html.Div([
        # instruction button to notify the user how to use the simulation tool

        dcc.Markdown(children='''There are three panels on the right: Survey, Transect Visualization and Power Calculation. The Survey tab contains a figure which shows all the DRM historical survey locations by year on the map. You can also use the **Select Files** button to select new survey data and update the figure. To begin with, you first click the **Start Simulation** button, then you will be asked to select a region to survey in the figure using the map selection tools on the top of the figure. Notice that the map selection tool bar will only appear when you hover your mouse over the figure. The selected region represents the location you want to conduct your new survey. After that, the app will help you estimate the proportion cover of the coral inside this region based on the historical survey data, and you are required to select a point process from which the coral will be simulated inside the region. If you have questions about how the data will be generated under different point processes, you can checkout the ** Point Process Introduction ** tab. After selecting a point process, you then need to specify the parameters that characterize this point process.  Additionally, other parts such as the transect, disease prevalence, and coral size can also be customized.'''),

        html.Button('Start Simulation', id='button_select_region', n_clicks=0),

        # the instruction related to the above button
        dcc.Markdown(children='''
        Select a region on the right figure. The map selection tool bar will only appear when you hover your mouse over the figure. Box Select and Lasso Select are mostly used. Click the Box Select or Lasso Select button, then drag and drop on the figure.
        ''', id='text_select_region', style={"display": "none"}),

        # show the rough prop_cover density estimate based on the selected sites
        html.Div([], id='prop_cover_estimate', style={'display': 'none'}),

        # the hidden div which stores the prop cover estimation
        dcc.Store(id='store_prop_cover_estimation'),

        # which process is used to generate data
        dcc.Markdown(id='text_dropdown_select_process', children='''Select which point process will the coral be simulated from.''', style={"display": "none"}),

        generate_dropdown_selection(),

        # based on selected process, let user specify the parameter of the process
        dcc.Markdown(id='text_input_process_parameters', children='''
                Specify the parameters of the certain point process under which the coral is simulated. Also specify other inputs like disease prevalence, and the transect. For how different parameters change the look of a certain point process, you can checkout the **Point Process Introduction** section. There is a playground at the bottom. For a given point process, you can adjust the parameters to see how the simulation data changes spatially. Finally, if you find one simulation under a combination of parameters is quite realistic, you can use the **port** function to copy these parameters to here below.''', style={"display": "none"}),

        # user-input area
        # html.Div(id='input_process_parameters', style={"display": "none"}),

        generate_user_input(),

        # empty line
        html.Br(),

        # button to simulate the corals or calculate the power of the method
        html.Div([
            html.Button('Simulate once',
                        id='button_start_simulation',
                        n_clicks=0,

                        ),
            html.Button(
                    'Calculate power',
                    id='button_power_calculation',
                    n_clicks=0
                )


            ],id='show_two_buttons',style={'display':'none'})
           ,
        # dbc.Spinner(html.Div(id='loading-output'), color='primary'),
        # html.Div([dbc.Spinner(color='primary')]),

        # instruction for power calculation
        dcc.Markdown(
            id='text_power_calculation_instruction',
            children='''
                  Calculate power''',
            style={'display': 'none'}
        ),
        html.Br()

    ],className='col-sm-5')


def generate_dropdown_selection():
    "return a Div containing the dropdown selection box"
    return dcc.Dropdown(
        id='dropdown_select_process',
        style={"display": "none"},
        options=[
            {'label': 'Homogeneous Poisson process', 'value': 1},
            {'label': 'Inhomogeneous Poisson process', 'value': 2},
            {'label': 'Cluster process', 'value': 3},
            # {'label': 'Strauss process', 'value': 4}
        ],
        # set the initial value=0 to hide the user input interface
        value=0)



def generate_user_input():
    "return a Div containing users' input interface"


    input_n_toolkits = html.Div(html.Div([html.A('Number of transects:', className='col-sm-4'),
                                                  dcc.Input(
                                                      type='number',
                                                      placeholder=2,
                                                      value = 2,
                                                      id='input_n_toolkits',
                                                      className='col-sm-4'

                                                  )
                                                  ], className='row'), id='input_n_toolkits_container', style={'display': 'none'})

    # slider
    # input_n_toolkits = html.Div(html.Div([
    #     html.A("Number of transects",className='col-sm-4'),
    #                              dcc.Slider(min=1,
    #                                         max=5,
    #                                         step=1,
    #                                         value=2,
    #                                         marks={i: '{}'.format(i) for i in range(1, 6)},
    #                                         id='input_n_toolkits',
    #                                         className='col-sm-4')
    #                              ], className='row'), id='input_n_toolkits_container',
    #                             className='row',
    #                             style={'display': 'none'})


    input_disease_prevalence = html.Div(html.Div([html.A('disease prevalence: ', id='input_disease_prevalence_tooltip', className='col-sm-4'),
                                     dcc.Input(

                                         type='number',
                                         placeholder=0.1,
                                         value = 0.1,
                                         step=0.1,
                                         min=0,
                                         max=1,
                                         id='input_disease_prevalence',
                                         className='col-sm-4'

                                     )
                                     ], className='row'), id='input_disease_prevalence_container', style={'display': 'none'})

    input_disease_prevalence_tooltip = dbc.Tooltip('the proportion of corals which get infected by a disease', target='input_disease_prevalence_tooltip')

    # text or number input
    input_fun_lambda = html.Div(html.Div([html.A('proportion cover function:', className='col-sm-4'), dcc.Input(
        id="input_fun_lambda",
        type='text',
        placeholder="1000 * np.exp(-(((x - 50) / 50) ** 2 + ((y - 50) / 50) ** 2) / 0.5 ** 2)",
        value="1000 * np.exp(-(((x - 50) / 50) ** 2 + ((y - 50) / 50) ** 2) / 0.5 ** 2)",
        className='col-sm-4'
    )],className='row'),id='show_input_fun_lambda',style={'display':'none'})

    input_parent_prop = html.Div(html.Div([html.A('parent corals / total corals:', className='col-sm-4'), dcc.Input(
        id="input_parent_prop",
        type='number',
        placeholder=0.01,
        value=0.01,
        step=0.01,
        className='col-sm-4'
    )],className='row'),id='show_input_parent_prop',style={'display':'none'})

    input_parent_range = html.Div(html.Div([html.A('parent range:', className='col-sm-4'), dcc.Input(
        id="input_parent_range",
        type='number',
        placeholder=5,
        value=5,
        className='col-sm-4'
    )],className='row'),id='show_input_parent_range',style={'display':'none'})

    input_strauss_beta = dcc.Input(
        id="input_strauss_beta",
        type='number',
        placeholder="strauss_beta",
        style={'display': 'none'}
    )
    input_strauss_gamma = dcc.Input(
        id="input_strauss_gamma",
        type='number',
        placeholder="strauss_gamma",
        style={'display': 'none'}
    )
    input_strauss_R = dcc.Input(
        id="input_strauss_R",
        type='number',
        placeholder="strauss_R",
        style={'display': 'none'}
    )

    input_transect_length = html.Div(html.Div([html.A('transect width (m): ', className='col-sm-4'),
                                      dcc.Input(

                                          type='number',
                                          placeholder=25,
                                          value=25,
                                          id='dcc_input_transect_length',
                                          className='col-sm-4'
                                      )
                                      ], className='row'), id='input_transect_length', style={'display': 'none'})



    input_transect_width = html.Div(html.Div([html.A('transect length (m): ', className='col-sm-4'),
                                     dcc.Input(

                                         type='number',
                                         placeholder=6,
                                         value = 6,
                                         id='dcc_input_transect_width',
                                         className='col-sm-4'

                                     )
                                     ], className='row'), id='input_transect_width', style={'display': 'none'})




    line_intercept_ratio = html.Div(html.Div([html.A('transect width / plot width', className='col-sm-4'),
                                     dcc.Input(
                                         type='number',
                                         placeholder=1/5,
                                         value = 1/5,
                                         step=0.1,
                                         id='dcc_line_intercept_ratio',
                                         className='col-sm-4')
                                     ],className='row'), id='line_intercept_ratio', style={'display': 'none'})

    coral_size = html.Div(html.Div([html.A('coral size (m^2): ', id='coral_size_tooltip',className='col-sm-4'),
                           dcc.Input(
                               type='number',
                               placeholder=0.0068,
                               value = 0.0068,
                               step=0.0001,
                               id='coral_size',
                               className='col-sm-4'
                           )
                           ],className='row' ),
                          id='coral_size_input',
                          style={'display': 'none'})

    coral_size_tooltip = dbc.Tooltip('the average size of an individual coral, measured in m^3', target='coral_size_tooltip')

    coral_size_std = html.Div(html.Div([html.A('coral size standard error: ', id='coral_size_std_tooltip', className='col-sm-4'),
                           dcc.Input(
                               type='number',
                               placeholder=0.001,
                               value = 0.001,
                               step=0.001,
                               id='coral_size_std',
                               className='col-sm-4'

                           )], className='row')
                           , id='coral_size_std_input', style={'display': 'none'})

    coral_size_std_tooltip = dbc.Tooltip('the standard deviation of the average size of an individual coral', target='coral_size_std_tooltip')

    prop_cover = html.Div(html.Div([html.A('proportion cover: ', className='col-sm-4', id='prop_cover_tooltip'),
                           dcc.Input(
                               type='number',
                               placeholder=0,
                               value = 0,
                               step=0.01,
                               min=0,
                               max=1,
                               id='prop_cover',
                               className='col-sm-4'
                           )
                           ],className='row'), id='prop_cover_input', style={'display': 'none'})

    prop_cover_tooltip = dbc.Tooltip('Proportion cover of coral. If it equals 0, its estimation based on the historical data will be used in the simulation', target='prop_cover_tooltip')

    num_of_replications = html.Div(html.Div([html.A('number of replications', className='col-sm-4'),
                                    dcc.Input(
                                        type='number',
                                        placeholder=10,
                                        value = 10,
                                        step=1,
                                        min=1,
                                        id='num_of_replications',
                                        className='col-sm-4'
                                    )
                                    ],className='row'), id='number_of_replications_input', style={'display': 'none'})


    return html.Div([
        input_n_toolkits,
        prop_cover,
        prop_cover_tooltip,
        input_fun_lambda,
        coral_size,
        coral_size_tooltip,
        coral_size_std,
        coral_size_std_tooltip,
        input_disease_prevalence,
        input_disease_prevalence_tooltip,
        input_parent_prop,
        input_parent_range,
        input_strauss_beta,
        input_strauss_gamma,
        input_strauss_R,
        input_transect_length,
        input_transect_width,
        line_intercept_ratio,
        num_of_replications
    ], id='input_process_parameters')