import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def generate_point_process_introduction():
    intro_text = dcc.Markdown(id='point_process_intro_text', children='''
#### How to use?
Click on the tab for the point process model to use to generate coral colonies.  The user can then specify the 1) proportion coral cover in the area of interest. 2) the disease prevalence (i.e., proportion of diseased corals in the area of interest). Once the parameters are all successfully selected, click the Start Simulation button.  An interactive map will be generated that shows the distribution of healthy and diseased coral colonies generated by the simulation. The user can try different configurations until the generated distribution matches the user’s desired coral distribution for their survey area. Once the correct distribution is chosen.  Click the Port Parameters button to send the selected distribution to the Simulation tab to examine the power of various survey designs for a study area with the selected distribution of coral colonies.
    
                  ''')


    intro_tab = html.Div([
        html.Div(dcc.Tabs([

        dcc.Tab(label='Homogeneous poisson process', children=[generate_homogeneous_poisson_process()
                                          ]),

        dcc.Tab(label='Inhomogeous poisson process', children=[
            generate_inhomogeneous_poisson_process()
        ]),
        dcc.Tab(label="Poisson clustering process", children=[
            generate_poisson_clustering_process()])

    ],id='intro_tab'),className='col-sm-6'),
    html.Div(className='col-sm-6')],
    className='row')

    button = html.Button('Start Simulation', id='intro_button_1', n_clicks=0)

    port = html.Button('Port parameters', id='intro_port', n_clicks=0)

    port_tooltip = dbc.Tooltip('Copy these parameter values to the Simulation Section', target='intro_port')  # hover text on port




    return html.Div([html.Br(), intro_text, intro_tab, html.Br(), button, port, port_tooltip])

# def generate_point_process_introduction():
#     intro_text = dcc.Markdown(id='point_process_intro_text', children='''
#
# #### Homogeneous poisson process
#
#
# A homogeneous poisson process with intensity lambda is the basic 'reference' or 'benchmark' model of a point process, which is sometimes called Complete Spatial Randomness. Its basic properties are: the number of points falling in any region A has a Poisson distribution with mean lambda x area(A); given that there are n points inside region A, the locations of these points are i.i.d and uniformly distributed inside A; the contents of two disjoint regions A and B are independent.
#
# One can adjust lambda to see how the point process changes.
#
# #### Inhomogeneous poisson process
#
# In general the intensity of a inhomogeneous Poisson process will vary from place to place, so the expected number of points falling in a small region of area depends on the intensity rate at that region characterized by the intensity function. Other properties follow the same as the homogeneous poisson process.
#
# One can input different intensity rate functions to see how the point process changes.
#
# #### Poisson clustering process
#
# In a Poisson cluster process, we begin with a Poisson process Y of 'parent' points. Each parent point then givens rise to a finite set of 'offspring' points according to some stochastic mechanism. The set comprising all the offspring points forms a point process X. Only X is observed. An example is the Matern cluster process in which the parent points come from a homogeneous Poisson process with intensity k, and each parent has a Poisson(u) number of offspring, independently and uniformly distributed in a disc of radius r centered around the parent. Here, we provide an interactive plot of the Matern cluster process, one can input different parent intensity rate and offspring intensity rate to see how the point process changes.
#
#                   ''')
#
#
#     intro_tab = html.Div([
#         html.Div(dcc.Tabs([
#
#             dcc.Tab(label='Homogeneous poisson process', children=[generate_homogeneous_poisson_process()
#                                                                    ]),
#
#             dcc.Tab(label='Inhomogeous poisson process', children=[
#                 generate_inhomogeneous_poisson_process()
#             ]),
#             dcc.Tab(label="Poisson clustering process", children=[
#                 generate_poisson_clustering_process()])
#
#         ],id='intro_tab'),className='col-sm-6'),
#         html.Div(className='col-sm-6')],
#         className='row')
#
#     button = html.Button('Start Simulation', id='intro_button_1', n_clicks=0)
#
#     port = html.Button('Port parameters', id='intro_port', n_clicks=0)
#
#     port_tooltip = dbc.Tooltip('Copy these parameter values to the Simulation Section', target='intro_port')  # hover text on port
#
#
#
#
#     return html.Div([html.Br(), intro_text, intro_tab, html.Br(), button, port, port_tooltip])
def generate_homogeneous_poisson_process():

    blank_line = html.Br()



    lambda_adj = html.Div([
        dcc.Markdown('''proportion cover''', className='col-sm-6'),
        dcc.Input(
        id='intro_lambda',
        type='number',
        placeholder=0.03,
        value=0.03,
        min=0,
        max=1,
        className='col-sm-6'
    )], className='row')

    disease_rate = html.Div([
        dcc.Markdown('''disease prevalence''', className='col-sm-6'),
        dcc.Input(
        id='intro_prevalence_rate',
        type='number',
        placeholder=0.1,
        value=0.1,
        step=0.1,
        min=0,
        max=1,
        className='col-sm-6'
    )], className='row')

    coral_size = html.Div([
        dcc.Markdown('''coral size (m^2)''', className='col-sm-6'),
        dcc.Input(
            id='intro_coral_size',
            type='number',
            placeholder=0.0068,
            value=0.0068,
            step=0.0001,
            className='col-sm-6'
        )], className='row', style={'display':'none'})

    coral_size_std = html.Div([
        dcc.Markdown('''coral size standard deviation''', className='col-sm-6'),
        dcc.Input(
            id='intro_coral_size_std',
            type='number',
            placeholder=0.001,
            value=0.001,
            step=0.001,
            className='col-sm-6'
        )], className='row', style={'display':'none'})

    # button = html.Button('Start Simulation', id='intro_button_1', n_clicks=0)
    #
    # port = html.Button('Port parameters', id='intro_port', n_clicks=0)
    #
    # port_tooltip = dbc.Tooltip('Copy these parameter values to the Simulation Section', target='intro_port')  # hover text on port

    graph = dcc.Loading(dcc.Graph(id='homogeneous_poisson_process',style={'display':'none'}))


    text_info = html.Div([], id='text_homogeneous_poisson_process')

    return html.Div([blank_line, lambda_adj, coral_size, coral_size_std, disease_rate, graph, text_info])

def generate_inhomogeneous_poisson_process():

    blank_line = html.Br()

    input_fun_lambda = html.Div([
        dcc.Markdown('''intensity rate function''', className='col-sm-6'),

        dcc.Input(
        id="intro_fun_lambda",
        type='text',
        placeholder="1000 * np.exp(-(((x - 50) / 50) ** 2 + ((y - 50) / 50) ** 2) / 0.5 ** 2)",
        value = "1000 * np.exp(-(((x - 50) / 50) ** 2 + ((y - 50) / 50) ** 2) / 0.5 ** 2)",
        className='col-sm-6'
    )
    ], className='row')

    coral_size = html.Div([
        dcc.Markdown('''coral size (m^2)''', className='col-sm-6'),
        dcc.Input(
            id='intro_coral_size_inhomogeneous',
            type='number',
            placeholder=0.0068,
            value=0.0068,
            step=0.0001,
            className='col-sm-6'
        )], className='row', style={'display':'none'})

    coral_size_std = html.Div([
    dcc.Markdown('''coral size standard deviation''', className='col-sm-6'),
    dcc.Input(
        id='intro_coral_size_std_inhomogeneous',
        type='number',
        placeholder=0.001,
        value=0.001,
        step=0.001,
        className='col-sm-6'
    )], className='row')
    disease_rate = html.Div([
        dcc.Markdown('''disease prevalence''', className='col-sm-6'),
        dcc.Input(
            id='intro_prevalence_rate_inhomogeneous',
            type='number',
            placeholder=0.1,
            value=0.1,
            step=0.1,
            min=0,
            max=1,
            className='col-sm-6'
        )], className='row', style={'display':'none'})

    graph = dcc.Loading(dcc.Graph(id='inhomogeneous_poisson_process', style={'display':'none'}))

    text_info = html.Div([], id='text_inhomogeneous_poisson_process')

    return html.Div([blank_line, input_fun_lambda, coral_size, coral_size_std, disease_rate,  graph, text_info])

def generate_poisson_clustering_process():
    blank_line = html.Br()
    input_coral_intensity = html.Div([
        dcc.Markdown('''proportion cover''', className='col-sm-6'),
        dcc.Input(
        id='intro_lambda_2',
        type='number',
        placeholder=0.03,
        value=0.03,
        step=0.01,
        min=0,
        max=1,
        className='col-sm-6'
    )], className='row')

    coral_size = html.Div([
        dcc.Markdown('''coral size (m^2)''', className='col-sm-6'),
        dcc.Input(
            id='intro_coral_size_poisson',
            type='number',
            placeholder=0.0068,
            value=0.0068,
            step=0.0001,
            className='col-sm-6'
        )], className='row', style={'display':'none'})

    coral_size_std = html.Div([
        dcc.Markdown('''coral size standard deviation''', className='col-sm-6'),
        dcc.Input(
            id='intro_coral_size_std_poisson',
            type='number',
            placeholder=0.001,
            value=0.001,
            step=0.001,
            className='col-sm-6'
        )], className='row', style={'display':'none'})

    input_parent_intensity = html.Div([
        dcc.Markdown('''parent corals / total corals''', className='col-sm-6'),
        dcc.Input(id='intro_parent_intensity', type='number', placeholder=0.01, value=0.01, step=0.01, className='col-sm-6')
    ],className='row')

    input_offspring_range = html.Div([
        dcc.Markdown('''parent range (m)''', className='col-sm-6'),
        dcc.Input(id='intro_offspring_range', type='number', placeholder=5, value=5,  className='col-sm-6')
    ],className='row')

    disease_rate = html.Div([
        dcc.Markdown('''disease prevalence''', className='col-sm-6'),
        dcc.Input(
            id='intro_prevalence_rate_3',
            type='number',
            placeholder=0.1,
            value=0.1,
            step=0.1,
            min=0,
            max=1,
            className='col-sm-6'
        )], className='row')

    graph = dcc.Loading(dcc.Graph(id='poisson_clustering_process',style={'display':'none'}))

    text_info = html.Div([], id='text_possion_clustering_process')



    return html.Div([blank_line, input_coral_intensity, coral_size, coral_size_std,  disease_rate, input_parent_intensity, input_offspring_range, graph, text_info])