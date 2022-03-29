import dash_core_components as dcc
import dash_html_components as html


def generate_power_calculation_result():
    "return a Div containing the result of the power calculation"
    text_power_calculation = dcc.Loading([html.Div(
        id='text_power_calculation',
        style={'display': 'block'},
        className='col-sm-10'
    )])

    intro_power_calculation = html.Div(dcc.Markdown('''
    For a fixed number of transects, we run repeated simulations to check what is the proportion of the confidence interval of our prediction covers the true parameters.
    '''),
        id='intro_power_calculation',
        style={'display':'block'})

    text_number_of_replications =  html.Div([],
                                            id='text_number_of_replications',
                                            style={'display':'block'})

    return html.Div([
        # empty line
        html.Br(),

        intro_power_calculation,

        text_number_of_replications,

        # position the text in center
        html.Div([ html.Div([], className='col-sm-1'),
                  text_power_calculation,
                   html.Div([], className='col-sm-1')
                   ], className='row')])


