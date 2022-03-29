import dash_core_components as dcc
import dash_html_components as html

def generate_survey_graph():
    "return a Div containing the graph of the survey"
    # a hidden div which holds the data
    data_stored = dcc.Store(id='data')

    # upload new data
    data_upload = html.Div([html.Div([],className='col-sm-3'),
              html.Div([
                  dcc.Upload(
                      id='upload-data',
                      children=html.Div([
                          html.A('Select Files')
                      ]),
                      style={
                          'width': '100%',
                          'height': '60px',
                          'lineHeight': '60px',
                          'borderWidth': '1px',
                          'borderStyle': 'dashed',
                          'borderRadius': '5px',
                          'textAlign': 'center',
                          'margin': '10px'
                      },
                      multiple=True
                  )
              ], className='col-sm-6')
                 ,
              html.Div([],className='col-sm-3'),], className='row')

    # figure
    figure = html.Div([
        # the coral site location maps
        html.Div([
            dcc.Graph(id='graph_data_visualization')
        ],
            className='col-sm-11',
            style={'padding-top': '1%'}
        ),
        # the year range slider
        html.Div([dcc.RangeSlider(id='RangeSlider-Year',
                                  vertical=True
                                  )], className='col-sm-1')
        # html.Div(['ddddd'], className='col-sm-6'),
        # html.Div(['dddddd'], className='col-sm-6')
    ], className='row')


    return html.Div([data_stored, data_upload, figure])

