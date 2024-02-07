from analiser__helper_functions import get_data, plot_on_map
from config_functions import get_config
import datetime

config = get_config()
data, line = get_data()


def create_2signs(n):
    if n < 10:
        return '0' + str(n)
    return str(n)


def create_time(hours, minutes, seconds):
    return (create_2signs(hours) + ':' +
            create_2signs(minutes) + ':' +
            create_2signs(seconds))


def move_time(hours, minutes, seconds, diff):
    seconds = seconds + diff
    if seconds >= 60:
        minutes = minutes + seconds // 60
        seconds = seconds % 60
        if minutes >= 60:
            hours = (hours + minutes // 60) % 24
            minutes = minutes % 60
    return hours, minutes, seconds


def pick_hms(date):
    """Returns hours, minutes, seconds"""
    hours, minutes, seconds = map(int, datetime.datetime.strftime(datetime.datetime.strptime(
        date, "%Y-%m-%d %H:%M:%S"), "%H:%M:%S").split(':'))
    return hours, minutes, seconds


def drop_date(date):
    hours, minutes, seconds = pick_hms(date)
    return create_time(hours, minutes, seconds)


if line != '':
    data = data[data['Lines'] == line]
print("First recorded date: " + data['Time'].min() + ", last recorded date: " + data['Time'].max())
while True:
    t = input("Moment to capture buses from (format: HH:MM:SS): ")
    try:
        h, m, s = map(int, t.split(':'))
        break
    except Exception:
        print("Not a valid format of time!")
h0, m0, s0 = move_time(h, m, s, -config['now_timediff'])
h1, m1, s1 = move_time(h, m, s, config['now_timediff'])
data['Time'] = data['Time'].apply(drop_date)
data = data[(create_time(h0, m0, s0) <= data['Time']) & (data['Time'] <= create_time(h1, m1, s1))]
print(data)
data['Legend'] = data['Lines']
plot_on_map(data, 'Lat', 'Latitude', 'Buses at around ' + t)
