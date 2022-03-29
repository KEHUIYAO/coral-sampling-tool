#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

data_raw = pd.read_csv("data/DRM Data 2005-2019.csv")
data = data_raw
data.Date = pd.to_datetime(data.Date)

# extract year from date
data['Year'] = data.Date.dt.to_period('Y')

# group by Site, count how many corals are sampled in each site
data = data[['Site', 'Latitude', 'Longitude', 'Year']]
data['count'] = 1
data.head(5)
data_unique = data.groupby('Site').aggregate({'Site': 'first', 'Latitude': 'first', 'Longitude': 'first', 'Year': 'first', 'count':'count'})

data_unique['Year'] = data_unique['Year'].astype(str)
data_unique.to_csv("data/data_cleaned.csv")







