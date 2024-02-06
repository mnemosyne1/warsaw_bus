import sys
import datetime
import pandas as pd
from collector__helper_functions import create_link, get_key, get_from_link

base = 'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e-927d-4ad3-9500-4ab9e55deb59'
key = get_key()
limit = 'type=1'  # only buses

collected, prev_list = [], []
prev_collected, prev_repeated, repeated, late = 0, 0, 0, 0
start_time = current_time = datetime.datetime.now()
link = create_link(base, key, limit)
while datetime.datetime.now() - start_time < datetime.timedelta(hours=3):
    try:
        current_time = datetime.datetime.now()
        new_list = get_from_link(link).json()['result']
        if new_list != prev_list:
            print(datetime.datetime.now() - start_time, file=sys.stderr)
            for bus in new_list:
                bustime = datetime.datetime.strptime(bus['Time'], "%Y-%m-%d %H:%M:%S")
                diff = current_time - bustime
                if diff > datetime.timedelta(seconds=20):
                    late = late + 1
                else:
                    collected.append(bus)
        else:
            print("Repeated", file=sys.stderr)
        prev_repeated = repeated
        prev_collected = len(collected)
        prev_list = new_list
    except Exception:
        print("Exception in operating on received data\n", file=sys.stderr)

df = pd.DataFrame(collected).drop_duplicates().reset_index(drop=True)
print(df)
filename = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '.csv'
df.to_csv(filename, index=False)
print(f'{late=}', file=sys.stderr)
print(f'{repeated=}', file=sys.stderr)
