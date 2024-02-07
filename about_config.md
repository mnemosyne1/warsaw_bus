In [config.json](config.json) you can set some useful values:
- collect_time: how long shall [collector_locations.py](collector_locations.py) work (default: 1 hour)
- late_record: how old records about bus locations you consider too old to be reliable (for example sometimes you can get 'info' dated to the previous day)
- min_time_diff: in [speed calculation](analiser_speed.py) what time difference between adjacent records is enough to calculate speed (has to be >0, shouldn't be too high)
- speed_limit: minimal speed to be plotted on the map, by default: what speed do you consider too high (used for stats about breaking the limit)
– default: 55 = 50 km/h (general speed limit) + 10%
- max_plausible_speed: what speed do you consider unreasonably high, meaning GPS records are trying to fool you – default: 90 km/h
- min_movement_speed: minimal value of speed to be considered in the speed histogram
- grid_precision: up to how many decimal places shall the coordinates be rounded when preparing a grid.
Default: 3. Values lower than 2 don't produce valuable info, as well as values above 5, but should not
break for any value ≥ 0
- high_percent: what percentage of buses should break the limit in the place to consider the limit 'often-broken' there.
Defaults to 50, can be adjusted anywhere between 0 and 100
- punctuality_start_delta: in [punctuality check](analiser_time.py) much time do you add a safety buffer in case bus has a negative delay at the beginning of your records.
Default: 2 minutes. Reasonable values: from 0 to 5 minutes
- dist_from_stop: punctuality check assumes bus in on the stop if distance between the stop and the closest point
on the line between records is less than this. Default: 80 metres, should be quite fine in range [50, 200]
- min_delay: what delay is too low to be considered in the stats. Default: -5 minutes, because I consider such haste unrealistic
- max_delay: self-explanatory. Default: 1 hour (again, realism reasons)
- far_from_stop: when we miss the stop (due to too low dist_from_stop), we need to get back on the track. 
Distance from the checked stop is one of two factors taken into account in the script to find such situations – by default it is above 500 metres
- highest_count: in [bus counter](analiser_count.py) set top limit for number. Helps in fighting depots
from dominating your map by outnumbering the streets. Default: 1000.
From my observations depots may produce approx. 3k/hour, up to 5k/h at night, streets: up to 400/h