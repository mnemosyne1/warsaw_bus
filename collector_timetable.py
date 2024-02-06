import sys
import pandas as pd
from collector__helper_functions import get_key, get_from_link


def create_stop_link(stop_id, nr, lin, apikey):
    return ('https://api.um.warszawa.pl/api/action/dbtimetable_get?'
            'id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId=' + stop_id
            + '&busstopNr=' + nr + '&line=' + lin + '&apikey=' + apikey)


print('Do not even think about having this script finishing before the heat'
      'death of the Universe (or at least half a day)', file=sys.stderr)
key = get_key()
link = 'https://api.um.warszawa.pl/api/action/public_transport_routes/?apikey=' + key
response = get_from_link(link)
flat_data = {'brigade': [], 'time': [], 'line': [], 'stop': [], 'stopno': []}
i = 0
for line in response.json()['result']:
    if len(line) < 3:
        print("Skipped " + line, file=sys.stderr)
        continue  # skips trams and the majority of trains
    print(str(i) + ' ' + line, file=sys.stderr)
    i = i + 1
    for route in response.json()['result'][line]:
        for stop in response.json()['result'][line][route].values():
            newlink = create_stop_link(stop['nr_zespolu'], stop['nr_przystanku'], line, key)
            newresponse = get_from_link(newlink)
            for lis in newresponse.json()['result']:
                for v in lis['values']:
                    if v['key'] == 'brygada':
                        flat_data['brigade'].append(v['value'])
                    elif v['key'] == 'czas':
                        flat_data['time'].append(v['value'])
                flat_data['line'].append(line)
                flat_data['stop'].append(stop['nr_zespolu'])
                flat_data['stopno'].append(stop['nr_przystanku'])
pd.DataFrame(flat_data).to_csv('timetable.csv', index=False)
