_Assignment (in Polish) may be found [here](assignment.md)_

_*.csv files with collected data that can serve as tests are available [here](https://drive.google.com/drive/folders/1dAod8YH3OrEe4XnB0qQPPMz5AHxWntuR?usp=sharing)_

# Manual
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
in there is a file called timetable_coords.csv – normally produced by [stopinfocombiner.py](stopinfocombiner.py)
### Other
For now – none. But probably coming soon

# The project is still in development.

## TODO list:
- test the punctuality analiser (from what I've checked, this should work on
[this file](https://drive.google.com/file/d/1OO0abfNr4qOItiduZ1uYgVg9JNRAl3Cy/view?usp=sharing),
almost not tested on others so no guarantees yet)
- prepare the code to be installable with pip install
- probably try to split check_brigade function in [analiser_time.py](analiser_time.py)
- remove commented code, have all other comments be in one language

## Known issues:
- Timetables don't save when they were downloaded – can work improperly when timetables are changed
- [Punctuality check](analiser_time.py) will not work with downloaded data if the day is changing during the observed period
- Warsaw API + GPS systems in buses are doing a lot of silly things, so probably some of them also can cause unexpected behaviours
- Scripts generally don't check what they get, so if they're given nonsense they'll work on it – and produce nonsense
- Calculating the speed in [analiser_speeed.py](analiser_speed.py) is quite long (time mostly consumed by the geodesic function if I'm not mistaken)
- ...


## TODO possible ideas:
- histogram of bus speeds
- map showing all buses at one particular moment
- maybe some regression of speed from geographical coordinates