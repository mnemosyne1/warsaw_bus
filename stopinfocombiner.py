import pandas as pd

timetable = pd.read_csv('timetable.csv', dtype={"brigade": str, "line": str})
stop_coords = pd.read_csv('stopinfo.csv')
(pd.merge(timetable, stop_coords).drop(['stop', 'stopno'], axis=1).
 to_csv('timetable_coords.csv', index=False))
