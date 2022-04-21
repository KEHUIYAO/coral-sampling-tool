from main import app
from layouts import layout
from callbacks import callback

app.layout = layout.generate_layout()
#app.run_server(debug=True, host='127.0.0.1')
server = app.server  # if using heroku
app.run_server(debug=True)  # if using heroku