from analiser__helper_functions import get_data, plot_on_map, plot_grid_static
from config_functions import get_config
import pandas as pd
import sys

config = get_config()
data, line = get_data()
loc_counter = {}

for index, r in data.iterrows():
    if line == '' or r['Lines'] == line:
        map_index = (round(r['Lon'], config['grid_precision']), round(r['Lat'], config['grid_precision']))
        if map_index not in loc_counter:
            loc_counter[map_index] = 0
        loc_counter[map_index] = loc_counter[map_index] + 1

grid_df = pd.DataFrame(list(loc_counter.keys()), columns=['Lon', 'Lat'])
grid_df['Legend'] = (list(loc_counter.values()))
grid_df['Legend'] = grid_df['Legend'].clip(upper=config['highest_count'])
grid_df = grid_df.sort_values(by='Legend')
print(grid_df, file=sys.stderr)
plot_on_map(grid_df, 'Legend', 'Bus count',
            'Number of bus records in given location')
