"""
Used NOAA's data, with token as done in directory 'dashboard_hw3'
Merging both stations data sets, both contain MA only data.
    - to gain latitude and longitude data of stations for geospatial data
"""
import pandas as pd

df_stations = pd.read_csv('stations_ma.csv')
df_stats = pd.read_csv('northeast_2025_daily.csv')
df_stations = df_stations.rename(columns={'id': 'station_id'})
df_stats = df_stats.rename(columns={'station': 'station_id'})
df_both = pd.merge(df_stats, df_stations, on='station_id', how='left')
print(df_both.head())

df_both.to_csv('ma_data.csv')
