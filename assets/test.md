![transect_line](https://i.imgur.com/eZLreAj.jpg)



# Line intercept method

Diver lays out a 10-25 m line. At intervals, substrate is characterized as 'coral', 'sand', 'algae', 'rubble'. For Point intercept, substrate is recorded at each 10 cm interval. For the Line intercept, substrate is recorded at length intervals (e.g. 0-5 cm-'coral'; 5-13 cm-'Sand', 13-28 cm-'coral', etc.). Point intercepts are faster to do than line, (important consideration when air is limiting).

# Coral colony counts

Within a 1 x 10 to 1x 25 m belt, diver counts all coral colonies to genus and if time allows, sizes them to <=5cm, >5-10cm, >10-20cm, >20-40cm, >40-80cm, >80-160cm, >160cm.

# Lesions

Within a 6 x 25 m belt, diver records all corals with lesions (tissue loss, discoloration, growth anomalies) by coral genus and size class.



```
html.Div(html.Div([html.A('transect width: ', className='col-sm-4'),
                                  dcc.Input(

                                      type='number',
                                      placeholder=25,
                                      value=25,
                                      id='dcc_input_transect_length',
                                      className='col-sm-4'
                                  )
                                  ], className='row'), id='input_transect_length', style={'display': 'none'})
```