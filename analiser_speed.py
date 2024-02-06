from geopy.distance import geodesic
import datetime
import sys
from analiser__helper_functions import get_data, plot_on_map, plot_histogram
from config_functions import get_config


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
    plot_on_map(speed_df, 'Speed', 'Speed')


config = get_config()
general_df, bus = get_data()
analise_speed(general_df, bus)
