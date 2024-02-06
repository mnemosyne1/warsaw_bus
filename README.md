_Assignment (in Polish) may be found [here](assignment.md)_

_*.csv files with collected data that can serve as tests are available [here](https://drive.google.com/drive/folders/1dAod8YH3OrEe4XnB0qQPPMz5AHxWntuR?usp=sharing)_

# Manual
## Config file
In [config.json](config.json) you can set some useful values:
- collect_time: how long shall [collector_locations.py](collector_locations.py) work (default: 1 hour)
- late_record: how old records about bus locations you consider too old to be reliable (for example sometimes you can get 'info' dated to the previous day)
- min_time_diff: in [speed calculation](analiser_speed.py) what time difference between adjacent records is enough to calculate speed (has to be >0, shouldn't be too high)
- speed_limit: minimal speed to be plotted on the map, by default: what speed do you consider too high (used for stats about breaking the limit)
– default: 55 = 50 km/h (general speed limit) + 10%
- max_plausible_speed: what speed do you consider unreasonably high, meaning GPS records are trying to fool you – default: 90 km/h
- min_movement_speed: minimal value of speed to be considered in the speed histogram
- punctuality_start_delta: in [punctuality check](analiser_time.py) much time do you add a safety buffer in case bus has a negative delay at the beginning of your records.
Default: 2 minutes. Reasonable values: from 0 to 5 minutes
- dist_from_stop: punctuality check assumes bus in on the stop if distance between the stop and the closest point
on the line between records is less than this. Default: 80 metres, should be quite fine in range [50, 200]
- min_delay: what delay is too low to be considered in the stats. Default: -5 minutes, because I consider such haste unrealistic
- max_delay: self-explanatory. Default: 1 hour (again, realism reasons)
- far_from_stop: when we miss the stop (due to too low dist_from_stop), we need to get back on the track. 
Distance from the checked stop is one of two factors taken into account in the script to find such situations – by default it is above 500 metres
## Downloading the data
### Bus locations
Run the [script](collector_locations.py) with your apikey, that's it
### Timetables
[Download](collector_timetable.py) the timetables into timetable.csv (warning – this takes reaaaally long due to the way Warsaw API about it is constructed)

To [decode](stopinfocombiner.py) this, you'll also need info about stops - downloaded with [this script](collector_locations.py)
## Operating on data
### Speeding
Run the [script](analiser_speed.py) giving it a .csv file with locations, see the results
### Punctuality
Run the [script](analiser_time.py) giving it a .csv file with locations. It silently assumes that in a directory it's called
in there is a file called timetable_coords.csv – usually produced by [stopinfocombiner.py](stopinfocombiner.py)
### Other
For now – none. But probably coming soon

# The project is still in development.

## TODO list:
- prepare the code to be installable with pip install
- probably try to split check_brigade function in [analiser_time.py](analiser_time.py)
- remove commented code, have all other comments be in one language
- ...

## Known issues:
- Timetables don't save when they were downloaded – can work improperly when timetables are changed
- [Punctuality check](analiser_time.py) will not work with downloaded data if the day is changing during the observed period
- Warsaw API + GPS systems in buses are doing a lot of silly things, so probably some of them also can cause unexpected behaviours
- Scripts generally don't check what they get, so if they're given nonsense they'll work on it – and produce nonsense
- Calculating the speed in [analiser_speeed.py](analiser_speed.py) is quite long (time mostly consumed by the geodesic function if I'm not mistaken)
- ...


## TODO possible ideas:
- histogram of bus speeds
- visualisation of delays
- map showing all buses at one particular moment
- maybe some regression of speed from geographical coordinates
- ...

# Credits
warsaw geojson file was copied from [this repo](https://github.com/andilabs/warszawa-dzielnice-geojson)