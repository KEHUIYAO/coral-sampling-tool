import dash
import pandas as pd
app = dash.Dash(__name__)

# load data
data = pd.read_csv("data/data_cleaned.csv")
data['Year'] = data['Year'].astype(str)
