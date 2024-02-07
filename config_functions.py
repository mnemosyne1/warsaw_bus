import json
import datetime


def create_config():
    default_config = {
        'collect_time': str(datetime.timedelta(hours=1, minutes=0, seconds=0)),
        'late_record': str(datetime.timedelta(hours=0, minutes=0, seconds=20)),
        'min_time_diff': 5,
        'speed_limit': 55,
        'max_plausible_speed': 90,
        'min_movement_speed': 10,
        'grid_precision': 3,
        'high_percent': 20,
        'punctuality_start_delta': 2,
        'dist_from_stop': 80,
        'min_delay': -300,
        'max_delay': 3600,
        'far_from_stop': 500
    }
    with open('config.json', 'w') as config:
        json.dump(default_config, config, indent=4)


def pick_hms(date):
    """Returns hours, minutes, seconds"""
    hours, minutes, seconds = map(int, date.split(':'))
    return hours, minutes, seconds


def get_config():
    """Returns consts defined in config.json"""
    with open('config.json', 'r') as config:
        ans = json.load(config)
        h, m, s = pick_hms(ans['collect_time'])
        ans['collect_time'] = datetime.timedelta(hours=h, minutes=m, seconds=s)
        h, m, s = pick_hms(ans['late_record'])
        ans['late_record'] = datetime.timedelta(hours=h, minutes=m, seconds=s)
        return ans


if __name__ == '__main__':
    create_config()
