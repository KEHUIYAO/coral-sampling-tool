from main import app
from layouts import layout
from callbacks import callback
server = app.server  # if using heroku
app.layout = layout.generate_layout()

# Run app and display result inline in the notebook
if __name__ == '__main__':
    #app.run_server(debug=True, host='127.0.0.1')
    app.run_server(debug=True)  # if using heroku