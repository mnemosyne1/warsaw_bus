import sys
import datetime
import pandas as pd
from collector__helper_functions import create_link, get_key, get_from_link
from config_functions import get_config

base = 'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e-927d-4ad3-9500-4ab9e55deb59'
key = get_key()
limit = 'type=1'  # only buses
config = get_config()

collected, prev_list = [], []
late = 0
link = create_link(base, key, limit)
start_time = current_time = datetime.datetime.now()
while datetime.datetime.now() - start_time < config['collect_time']:
    try:
        current_time = datetime.datetime.now()
        new_list = get_from_link(link).json()['result']
        if new_list != prev_list:
            print(datetime.datetime.now() - start_time, file=sys.stderr)
            for bus in new_list:
                bustime = datetime.datetime.strptime(bus['Time'], "%Y-%m-%d %H:%M:%S")
                diff = current_time - bustime
                if diff > config['late_record']:
                    late = late + 1
                else:
                    collected.append(bus)
        prev_list = new_list
    except Exception:
        print("Exception in operating on received data\n", file=sys.stderr)

df = pd.DataFrame(collected).drop_duplicates().reset_index(drop=True)
print(df)
filename = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '.csv'
df.to_csv(filename, index=False)
print(f'{late=}', file=sys.stderr)
