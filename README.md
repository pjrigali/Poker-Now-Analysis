# Poker Now Analsyis
[![Documentation Status](https://readthedocs.org/projects/poker-now-analysis/badge/?version=latest)](https://poker-now-analysis.readthedocs.io/en/latest/?badge=latest)

This is a package for analyzing past performance and player habits from the Poker Now website.

[Poker Now link](https://www.pokernow.club/)

Poker Now is a website that allows individuals to set up private poker tables.
The website allows you to download the data from the game. 
This package preforms NLP to parse the csv and creates a variety of objects for analyzing the game.

## Installation
[Pypi Documentation](https://pypi.org/project/warzone-analysis/)

The package can be accessed via pip install.

    pip install cold-war-zombies

## Usage
[Read the Docs](https://poker-now-analysis.readthedocs.io/en/latest/)

```python
import poker
from poker.base import Poker

# Input past Data folder location.
repo = '\\location of past Data folder'

# Manual grouping. When same players, play from different devices, they will get a different unique ID.
# This will group the players. 
grouped = [['YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS'],
           ['1_FRcDzJU-', 'ofZ3AjBJdl', 'yUaYOqMtWh', 'EIxKLHzvif'],
           ['3fuMmmzEQ-', 'LRdO6bTCRh', '9fNOKzXJkb'],
           ['FZayb4wOU1', '66rXA9g5yF', 'rM6qlbc77h', 'fy6-0HLhb_'],
           ['48QVRRsiae', 'u8_FUbXpAz'],
           ['Aeydg8fuEg', 'yoohsUunIZ'],
           ['mUwL4cyOAC', 'zGv-6DI_aJ'],
           ]

poker = Poker(repo_location=repo, grouped=grouped)
```

## Visualizations

The *Analyze* class will return the following plots:
* Damage Per Second
* Damage Per Max Ammo
* Damage Per Clip
* Time To Kill
* Shots To Kill

![Damage Per Second](https://miro.medium.com/max/1280/1*IyfMpo7OxpXGAm4MZd9t7Q.png)
![Damage Per Max Ammo](https://miro.medium.com/max/1280/1*eFT7lys6gkZMPO0LsOCQrA.png)
![Damage Per Clip](https://miro.medium.com/max/1280/1*Qtxn3jtbH0kRXICa7W2MfQ.png)
![Time To Kill](https://miro.medium.com/max/1280/1*VFABznePjcEVT_WdIPF5Og.png) 
![Shots To Kill](https://miro.medium.com/max/1280/1*vrw4BIZnm_mPw-V-OeXJwg.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
