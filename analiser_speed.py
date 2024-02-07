import pandas as pd
from geopy.distance import geodesic
import datetime
import sys
from analiser__helper_functions import get_data, plot_on_map, plot_histogram, plot_grid_static
from config_functions import get_config


config = get_config()
loc_speeds = {}


def calculate_speed(r):
    prev_time = datetime.datetime.strptime(r['P_time'], "%Y-%m-%d %H:%M:%S")
    new_time = datetime.datetime.strptime(r['Time'], "%Y-%m-%d %H:%M:%S")
    time_diff = (new_time - prev_time).total_seconds()
    if time_diff < config['min_time_diff']:
        return None
    distance = geodesic((r['P_lat'], r['P_lon']), (r['Lat'], r['Lon'])).km
    ans = distance / time_diff * 3600
    if ans > config['max_plausible_speed']:  # skips irrational values
        return None
    map_index = (round(r['Lon'], config['grid_precision']), round(r['Lat'], config['grid_precision']))
    if map_index not in loc_speeds:
        loc_speeds[map_index] = []
    loc_speeds[map_index].append(ans)
    return round(ans, 1)


def analise_speed(df, line):
    speed_df = df.drop('Brigade', axis=1).sort_values(by=['VehicleNumber', 'Time'])
    if line != '':
        speed_df = speed_df[speed_df['Lines'] == line]
    speed_df[['P_lat', 'P_lon', 'P_time']] = speed_df[['Lat', 'Lon', 'Time']].shift(1)
    speed_df = speed_df[speed_df.VehicleNumber.eq(speed_df.VehicleNumber.shift())]
    print("Calculating speeds... (this may be unexpectedly long)", file=sys.stderr)
    speed_df['Speed'] = speed_df.apply(calculate_speed, axis=1)
    print("Speeds calculated", file=sys.stderr)
    speed_df = speed_df.drop(['VehicleNumber', 'P_lat', 'P_lon', 'P_time'], axis=1).dropna()
    if bus != '':
        hist_title = 'Speeds of line ' + bus
    else:
        hist_title = 'Speeds of all lines'
    plot_histogram(speed_df[speed_df['Speed'] > config['min_movement_speed']]['Speed'], 'Speed', hist_title)
    speed_df = speed_df[speed_df['Speed'] > config['speed_limit']]
    speed_df['Legend'] = speed_df['Speed'].astype(str) + ': ' + speed_df['Lines'] + ', ' + speed_df['Time']
    plot_on_map(speed_df, 'Speed', 'Speed',
                'Places where recorded speed was above ' + str(config['speed_limit']))


general_df, bus = get_data()
analise_speed(general_df, bus)
loc_speeds_percent = {}
for square in loc_speeds:
    loc_speeds_percent[square] = round(sum(
        1 for value in loc_speeds[square] if value > config['speed_limit']) /
                                       len(loc_speeds[square]) * 100, 1)
    loc_speeds[square] = round(sum(loc_speeds[square]) / len(loc_speeds[square]), 1)
grid_df = pd.DataFrame(list(loc_speeds.keys()), columns=['Lon', 'Lat'])
grid_df['Legend'] = list(loc_speeds.values())
plot_on_map(grid_df, 'Legend', 'Average speed',
            'Average speed in locations', max(45 - 9 * config['grid_precision'], 5))
overspeed_grid_df = pd.DataFrame(list(loc_speeds_percent.keys()), columns=['Lon', 'Lat'])
overspeed_grid_df['Legend'] = list(loc_speeds_percent.values())
overspeed_grid_df = overspeed_grid_df[overspeed_grid_df['Legend'] > config['high_percent']]
plot_on_map(overspeed_grid_df, 'Legend', 'Average speed',
            'Locations where more than ' + str(config['high_percent']) + '% buses'
            ' had speed higher than ' + str(config['speed_limit']),
            max(45 - 9 * config['grid_precision'], 5))
# Example of use of plot_grid_static:
# plot_grid_static(loc_speeds, 'Average speed in locations')
