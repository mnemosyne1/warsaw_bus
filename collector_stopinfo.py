import pandas as pd
from collector__helper_functions import get_key, get_from_link

key = get_key()
link = 'https://api.um.warszawa.pl/api/action/dbstore_get?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey=' + key
response = get_from_link(link)
res = response.json()['result']
stop_data = {'stop': [], 'stopno': [], 'Lat': [], 'Lon': []}
for s in res:
    for v in s['values']:
        if v['key'] == 'zespol':
            stop_data['stop'].append(v['value'])
        elif v['key'] == 'slupek':
            stop_data['stopno'].append(v['value'])
        elif v['key'] == 'szer_geo':
            stop_data['Lat'].append(v['value'])
        elif v['key'] == 'dlug_geo':
            stop_data['Lon'].append(v['value'])
pd.DataFrame(stop_data).to_csv('stopinfo.csv', index=False)
