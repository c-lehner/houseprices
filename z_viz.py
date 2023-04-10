'''
File: z_viz.py
Author: C. Lehner
Vizualiation of scraped data
'''
import folium
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
import branca.colormap as cm
import pandas as pd
import numpy as np
import datetime
#read in csvs of housing data
dfnh1 = pd.read_csv("nhzillow.csv")
dfnh3 = pd.read_csv("nhzillow2.csv")
dfvt1 = pd.read_csv("vtzillow1.csv")
dfme1 = pd.read_csv("mezillow1.csv")
dfme2 = pd.read_csv("mezillow2.csv")
#combine dataframes
df = pd.concat([dfnh1, dfnh3, dfvt1,dfme1,dfme2], ignore_index=True)
#save as csv
# df.to_csv("zillow.csv", index=False)
#UnformattedPrice is the price of the house in dollars rounded
#drop duplicates of zpid
df = df.drop_duplicates(subset='zpid')
#save again
# df.to_csv("zillow.csv", index=False)
date_format = '%m/%d/%Y'
date_converter = lambda x: datetime.datetime.fromtimestamp(x/1000).strftime(date_format) if pd.notna(x) else None
df['dateSold'] = df['dateSold'].apply(date_converter)
#import zillowcols.csv, the csv I deleted a bunch of useless columns from
cols = pd.read_csv("zillowcols.csv")
#get the variable names from the csv
variables = cols.columns
#now subset df to only include the variables in the csv
df = df[variables]
colormap = cm.LinearColormap(colors=['green', 'yellow', 'red'], vmin=50, vmax=280)
map = folium.Map(location = [43.689613, -72.254524], tiles='Stamen Toner',
    zoom_start = 10)
#remove nulls from lat/long
df_n = df.dropna(subset=['latitude', 'longitude', 'taxAssessedValue', 'unformattedPrice', 'livingArea', 'bedrooms'])
#calculate price per square foot
df_n.loc[:,'price_per_sqft'] = df_n['taxAssessedValue']/df_n['livingArea']
#describe price per sqft
df_n['price_per_sqft'].describe()
#find outliers
df_n[df_n['price_per_sqft'] > 1000]
#remove outliers
df_n = df_n[df_n['price_per_sqft'] < 1000]
#add points to map
for i in range(0,len(df_n)):
    folium.Circle([df_n.iloc[i]['latitude'], df_n.iloc[i]['longitude']],
                        radius=80,
                        fill=True,
                        color=colormap(df_n.iloc[i]['price_per_sqft']),
                        fill_opacity=0.2, outline=False).add_to(map)
#add child
map.add_child(colormap)
#subset data for heatmap
df_hm = df_n[['latitude', 'longitude', 'price_per_sqft']]
# HeatMap(df_hm).add_to(map)
map.save("map3.html")

