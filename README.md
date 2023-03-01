# Poker Now Analysis
[![Documentation Status](https://readthedocs.org/projects/poker-now-analysis/badge/?version=latest)](https://poker-now-analysis.readthedocs.io/en/latest/?badge=latest)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/pjrigali/Poker-Now-Analysis?color=blue&label=commits&logoColor=blue)](https://github.com/pjrigali)

This is a package for analyzing past performance and player habits from the Poker Now website.

[Poker Now link](https://www.pokernow.club/)

Poker Now is a website that allows individuals to set up private poker tables.
The website allows you to download the data from the game. 
This package preforms NLP to parse the csv and creates a variety of objects for analyzing a poker game.

## Installation
In progress...

## Usage
[Read the Docs](https://poker-now-analysis.readthedocs.io/en/latest/)

```python
import poker
from poker.classes.poker import Poker

# Note self.
me = 'Peter @ Jf-Q4OmfIt'

# Input past Data folder location.
repo = '\\location of past Data folder'

# Manual grouping. When same players, play from different devices, they will get a different unique ID.
# This will group the players. 
grouped = {'Peter'   : ('mQWfGaGPXE', 'ijDyevyKYD', 'Jf-Q4OmfIt'),
        'Flynn'   : ('YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS', 'AAVEC4azwk'),
        'Mike'    : ('1_FRcDzJU-', 'ofZ3AjBJdl', 'yUaYOqMtWh', 'EIxKLHzvif', 'welPeANz41'),
        'Johnny'  : ('3fuMmmzEQ-', 'LRdO6bTCRh', '9fNOKzXJkb', '88zR6gcIvD'),
        'Robby'   : ('FZayb4wOU1', '66rXA9g5yF', 'rM6qlbc77h', 'fy6-0HLhb_', 'nlk80T6XeC'),
        'Carter'  : ('48QVRRsiae', 'u8_FUbXpAz'),
        'Pfanz'   : ('Aeydg8fuEg', 'yoohsUunIZ', 'pvow8N1-FT'),
        'Yuri'    : ('mUwL4cyOAC', 'zGv-6DI_aJ', 'DySJmToB8p'),
        'Brian'   : ('FgmbZrCA9u', 'K7wE-uWJaj', 'kNiVoJP5Ym'),
        'Henry'   : ('HiZcYKvbcw', 'GXxPFeJI6u'),
        'Kaz'     : ('e_guu9eD6Q', '4pYZ-YdlJa'),
        'Nate'    : ('uVSlQwPVtk', 'YDeMDTtJPl'),
        'Bryson'  : ('-qWOsSgvQM', 'HTi7AMTQNr'),
        'Jack'    : ('VnrRHVzTZy', 'twk14-WLnE'),
        'Baker'   : ('cKZ72RXCxd', 'uRb9uI6e8-'),
        'Sinclair': ('cjuTQ51KDm',),
        'Ryan'    : ('eR3DTX32e8',),
        'Robert'  : ('BSg5NL6pWI',)}

# line_limit and item_limit not necessary.
user_inputs = {'me': me, 'repo': repo, 'grouped': grouped, 'line_limit': 50, 'item_limit': 50}
p = Poker(user_inputs=user_inputs)
```

## Visualizations
In progress...

## Below are some write-ups utilizing the package.
![Time and Performance](https://miro.medium.com/max/700/1*AbNNC1xrWLb5XiswbRfiaQ.png)
[Time and Performance](https://medium.com/@peterjrigali/how-does-decision-time-affect-performance-in-poker-fde88f1adae9)
_Example of the package to run tests._


## Changelog
* *1.0.0* - Working package.
* *1.0.1* - Simplified package.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
