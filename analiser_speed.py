from geopy.distance import geodesic
import datetime
import sys
from analiser__helper_functions import get_data, plot_on_map


def calculate_speed(r):
    # print('Calculating for ' + r['Time'] + ', previous one being ' + r['P_time'] + ' on line ' + str(r['Lines']) +
    #      ' (current lat: ' + str(r['Lat']) + ', prev: ' + str(r['P_lat']) + ')', file=sys.stderr)
    prev_time = datetime.datetime.strptime(r['P_time'], "%Y-%m-%d %H:%M:%S")
    new_time = datetime.datetime.strptime(r['Time'], "%Y-%m-%d %H:%M:%S")
    time_diff = (new_time - prev_time).total_seconds()
    if time_diff <= 10:
        return None
    distance = geodesic((r['P_lat'], r['P_lon']), (r['Lat'], r['Lon'])).km
    ans = distance/time_diff * 3600
    if ans > 100:  # odsiewa oczywiste błędy systemu raportowania GPS
        return None
    return round(ans, 1)


def analise_speed(df):
    speed_df = df.drop('Brigade', axis=1).sort_values(by=['VehicleNumber', 'Time'])
    speed_df[['P_lat', 'P_lon', 'P_time']] = speed_df[['Lat', 'Lon', 'Time']].shift(1)
    speed_df = speed_df[speed_df.VehicleNumber.eq(speed_df.VehicleNumber.shift())]
    print("Calculating speeds... (this may be unexpectedly long)", file=sys.stderr)
    speed_df['Speed'] = speed_df.apply(calculate_speed, axis=1)
    print("Speeds calculated", file=sys.stderr)
    speed_df = speed_df.drop(['VehicleNumber', 'P_lat', 'P_lon', 'P_time'], axis=1).dropna()
    speed_df = speed_df[speed_df['Speed'] > 55]
    speed_df['Legend'] = speed_df['Speed'].astype(str) + ': ' + speed_df['Lines'] + ', ' + speed_df['Time']
    plot_on_map(speed_df, 'Speed', 'Speed')


general_df = get_data()
analise_speed(general_df)
