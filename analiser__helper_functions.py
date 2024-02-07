import argparse
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


def get_data():
    """Processes the data given as call arguments
        :returns: tuple of 1. DataFrame of collected data,
        2. number of line which is checked (or empty string for all lines)"""
    __parser = argparse.ArgumentParser()
    __parser.add_argument('datafile', help='name of file with bus records')
    __parser.add_argument('line', help='number of line to be checked (default = all)', default='', nargs='?')
    args = __parser.parse_args()
    __line = str.capitalize(args.line)
    with open(args.datafile, 'r') as datafile:
        res = pd.read_csv(datafile, dtype={'Lines': str, 'Brigade': str})
        if __line != '' and __line not in res['Lines'].values:
            exit('No records were found for the given line in the given file!')
        return res, __line


def plot_on_map(df, plotted, plotted_name, title, size=10):
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
        marker=dict(size=size, colorscale='viridis', color=df[plotted].astype('int64'),
                    colorbar=dict(title=plotted_name)),
        text=df.Legend
    ))
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lon=df.Lon.mean(), lat=df.Lat.mean()),
            zoom=9
        ),
        title=title
    )
    fig.show()


def plot_histogram(val, ox, title):
    """Creates a histogram of given data
    :param val: value to be plotted
    :param ox: title of x-axis
    :param title: title of histogram"""
    plt.hist(val)
    plt.xlabel(ox)
    plt.ylabel('Frequency')
    plt.title(title)
    plt.show()


def plot_grid_static(data, title):
    """Creates a static plot of given data (which should create some kind
    of grid from geographical coordinates)"""
    map_data = gpd.read_file('warszawa-dzielnice.geojson')
    fig, ax = plt.subplots()
    map_data.plot(ax=ax, alpha=0.5, color='grey')
    values = list(data.values())

    # Plot the values as squares with color scale
    for d in data:
        ax.plot(d[0], d[1], marker='s', color=plt.cm.viridis(data[d] / max(values)),
                markersize=10, transform=ax.transData)
    # ctx.add_basemap(ax, crs=map_data.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
    norm = Normalize(vmin=min(values), vmax=max(values))
    sm = ScalarMappable(cmap='viridis', norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Value')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    plt.grid(True)
    plt.show()
