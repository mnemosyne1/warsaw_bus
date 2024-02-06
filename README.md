_Assignment (in Polish) may be found [here](assignment.md)_

_*.csv files with collected data that can serve as tests are available [here](https://drive.google.com/drive/folders/1dAod8YH3OrEe4XnB0qQPPMz5AHxWntuR?usp=sharing)_

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
- Punctuality check will not work with downloaded data if the day is changing during the observed period
- Warsaw API + GPS systems in buses are doing a lot of silly things, so probably some of them also can cause unexpected behaviours
- Scripts generally don't check what they get, so if they're given nonsense they'll work on it – and produce nonsense
- Calculating the speed in [analiser_speeed.py](analiser_speed.py) is quite (time mostly consumed by the geodesic function if I'm not mistaken)
- ...


## TODO possible ideas:
- histogram of bus speeds
- map showing all buses at one particular moment
- maybe some regression of speed from geographical coordinates