_Assignment (in Polish) may be found [here](assignment.md)_

_*.csv files with collected data that can serve as tests are available [here](https://drive.google.com/drive/folders/1dAod8YH3OrEe4XnB0qQPPMz5AHxWntuR?usp=sharing)_

# Manual
## Config file
This manual got too long, so this part of it is now available [here](about_config.md)
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

# The project is still in development.

# TODO list:
- prepare the code to be installable with pip install
- probably try to split check_brigade function in [analiser_time.py](analiser_time.py)
- add better comments here and there

# Known issues:
- Timetables don't save when they were downloaded – can work improperly when timetables are changed
- [Punctuality check](analiser_time.py) will not work with downloaded data if the day is changing during the observed period
- Warsaw API + GPS systems in buses are doing a lot of silly things, so probably some of them also can cause unexpected behaviours
- Scripts generally don't check what they get, so if they're given nonsense they'll work on it – and produce nonsense
- Calculating the speed in [analiser_speeed.py](analiser_speed.py) is quite long (time mostly consumed by the geodesic function if I'm not mistaken)
- Plotting the grid doesn't actually produce grid, it creates a scatter of dots – that's caused by
the library used for plotting. If you want to have a grid, check plot_grid_static from [the same file](analiser__helper_functions.py).
That's ugly and slow, but produces squares, not dots – example of use is commented in [analiser_speeed.py](analiser_speed.py)
- ...

# TODO possible ideas:
- map showing all buses at one particular moment

# Credits
warsaw geojson file was copied from [this repo](https://github.com/andilabs/warszawa-dzielnice-geojson)