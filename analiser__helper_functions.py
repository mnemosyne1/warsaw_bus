import argparse
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go


def get_data():
    """Returns DataFrame of collected data, link to file with which should
        be given as an argument when calling the script"""
    __parser = argparse.ArgumentParser()
    __parser.add_argument('datafile', help='name of file with bus records')
    args = __parser.parse_args()
    with open(args.datafile, 'r') as datafile:
        return pd.read_csv(datafile, dtype={'Lines': str, 'Brigade': str})


def plot_on_map(df, plotted, plotted_name):
    """Creates a scatter plot on map of Warsaw. df given should have
     at least 4 columns: Lat, Lon, Legend, and the plotted one"""
    # original src file: https://github.com/andilabs/warszawa-dzielnice-geojson
    geojson_file = 'warszawa-dzielnice.geojson'
    warsaw_map = gpd.read_file(geojson_file)
    fig = go.Figure()

    fig.add_trace(go.Choroplethmapbox(
        geojson=warsaw_map.__geo_interface__,
        locations=warsaw_map.index,
        z=warsaw_map.index,
        colorscale='Viridis',
        marker=dict(opacity=0.3),
        showscale=False
    ))
    fig.add_trace(go.Scattermapbox(
        lat=df.Lat,
        lon=df.Lon,
        mode='markers',
        marker=dict(size=10, colorscale='viridis', color=df[plotted].astype('int64'),
                    colorbar=dict(title=plotted_name)),
        text=df.Legend
    ))
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lon=df.Lon.mean(), lat=df.Lat.mean()),
            zoom=9
        )
    )
    fig.show()
