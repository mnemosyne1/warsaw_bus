import pandas as pd
from analiser__helper_functions import get_data, plot_on_map
import os
from geopy.distance import geodesic
import datetime
import sys
import matplotlib.pyplot as plt


def define_checked(bus_list):
    bus_list = bus_list['Lines'].drop_duplicates()
    print(bus_list)
    filename = 'recorded_buses.csv'
    while True:
        try:
            bus_list.to_csv(filename, mode='x')
            break
        except FileExistsError:
            filename = '_' + filename
    print('Full list of recorded buses and brigades is available in file: ' + filename)
    while True:
        checked_line = str.capitalize(input('Number of line to be analysed: '))
        if not str(checked_line) in bus_list.values:
            print('No records were found for line ' + str(checked_line) + '!')
            continue
        os.remove(filename)
        return checked_line


def create_2signs(n):
    if n < 10:
        return '0' + str(n)
    return str(n)


def create_time(hours, minutes, seconds):
    return (create_2signs(hours) + ':' +
            create_2signs(minutes) + ':' +
            create_2signs(seconds))


def convert_to_time(time):
    hours, minutes, seconds = map(int, time.split(':'))
    return create_time(hours % 24, minutes, seconds)


def pick_hms(date):
    """Returns hours, minutes, seconds"""
    hours, minutes, seconds = map(int, datetime.datetime.strftime(datetime.datetime.strptime(
        date, "%Y-%m-%d %H:%M:%S"), "%H:%M:%S").split(':'))
    return hours, minutes, seconds


def drop_date(date):
    hours, minutes, seconds = pick_hms(date)
    return create_time(hours, minutes, seconds)


def get_stop_index(timetable, time):
    # print(time)
    hours, minutes, seconds = map(int, time.split(':'))
    # add 2 minutes in case bus is too early
    if minutes < 58:
        minutes = minutes + 2
    else:
        hours, minutes = hours + 1, (minutes + 2) % 60
    time = create_time(hours, minutes + 1, seconds)
    # print(time)
    time = timetable.loc[timetable['time'] > time]
    # print(tmp)
    return time.index[0]


def create_num_time(time):  # TODO: TMP
    h, m, s = map(int, time.split(':'))
    return 10000 * h + 100 * m + s


def closest_point(lat_point, lon_point, lat_line_start, lon_line_start, lat_line_end, lon_line_end):
    line_v = [lat_line_end - lat_line_start, lon_line_end - lon_line_start]
    point_v = [lat_point - lat_line_start, lon_point - lon_line_start]
    s = sum(a**2 for a in line_v)
    if s != 0:
        p = max(0.0, min(1.0, sum(a * b for a, b in zip(point_v, line_v)) / s))
        closest_point_lat = lat_line_start + p * (lat_line_end - lat_line_start)
        closest_point_lon = lon_line_start + p * (lon_line_end - lon_line_start)
    else:
        closest_point_lat = lat_line_start
        closest_point_lon = lon_line_start
    return geodesic((lat_point, lon_point), (closest_point_lat, closest_point_lon)).m


def check_brigade(data, table, brigade):
    table.index.name = 'idx'
    table = (table.loc[(table['line'] == bus) & (table['brigade'] == brigade)].
             sort_values(by=['time', 'idx']).drop_duplicates().reset_index(drop=True))
    table['time'] = table['time'].apply(convert_to_time)
    data = (data.loc[(data['Lines'] == bus) & (data['Brigade'] == brigade)].
            sort_values(by='Time').drop_duplicates().reset_index(drop=True))
    j = 0
    data['Time'] = data['Time'].apply(drop_date)
    i = get_stop_index(table, data['Time'][0])
    timetable_series = table.loc[i]
    location_series = data.loc[0]
    prev_lat, prev_lon = location_series['Lat'], location_series['Lon']
    s_dist = closest_point(timetable_series['Lat'], timetable_series['Lon'],
                           prev_lat, prev_lon,
                           location_series['Lat'], location_series['Lon'])
    while True:
        print('Record time: ' + location_series['Time'], file=sys.stderr)
        print('Next stop time: ' + timetable_series['time'], file=sys.stderr)
        cur_lat, cur_lon = location_series['Lat'], location_series['Lon']
        dist = closest_point(timetable_series['Lat'], timetable_series['Lon'],
                             prev_lat, prev_lon, cur_lat, cur_lon)
        if dist <= 80:
            print('Stop found!', file=sys.stderr)
            table_time = pd.to_timedelta(timetable_series['time'])
            actual_time = pd.to_timedelta(location_series['Time'])
            delay = (actual_time - table_time).total_seconds()
            if delay >= -300:  # else: value is unrealistic
                delays.append(delay / 60)
            i = i + 1
            if i == table.shape[0]:
                break
            timetable_series = table.loc[i]
            s_dist = closest_point(timetable_series['Lat'], timetable_series['Lon'],
                                   prev_lat, prev_lon, cur_lat, cur_lon)
        elif dist > 500 and dist > 2 * s_dist:  # we're far from stop and getting farther
            print('Skipping stop!', file=sys.stderr)
            i = get_stop_index(table, data['Time'][j])
            timetable_series = table.loc[i]
            s_dist = closest_point(timetable_series['Lat'], timetable_series['Lon'],
                                   prev_lat, prev_lon, cur_lat, cur_lon)
        else:
            print('Bus in move', file=sys.stderr)
            j = j + 1
            if j == data.shape[0]:
                break
            location_series = data.loc[j]
        if (location_series['Lat'], location_series['Lon']) != (cur_lat, cur_lon):
            prev_lat, prev_lon = cur_lat, cur_lon


def plot_delays(delay):
    plt.hist(delay)
    plt.xlabel('Delay')
    plt.ylabel('Frequency')
    plt.title('Delays of line ' + bus)
    plt.show()


ttable = pd.read_csv('timetable_coords.csv',
                     dtype={"brigade": str, "line": str})
ddata = get_data()
tracked_buses = ddata[['Lines', 'Brigade']].drop_duplicates().reset_index(drop=True)
bus = define_checked(tracked_buses)
delays = []
for brig in tracked_buses.loc[tracked_buses['Lines'] == bus]['Brigade']:
    check_brigade(ddata, ttable, brig)
plot_delays(delays)

