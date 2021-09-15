Intro
*****

.. meta::
   :description: Landing page for poker-now-analysis.
   :keywords: Poker, Python, Analysis, Texas Hold'em

This is a package for analyzing past performance and player habits from the Poker Now website.

`Pypi link <https://pypi.org/project/cold-war-zombies/>`_

.. code-block::

    pip install cold-war-zombies

Usage
-----
Building the package:

.. code-block:: python

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
Within **weapon_class_levels** and **perk_class_levels** you should input your tier level for the respective item.

For **Health** input the desired zombie level and current zombie health cap.

Set **outbreak** to True if you would like to look at the results for outbreak.

More Info
---------
`Github <https://github.com/pjrigali/Call-Of-Duty-Cold-War-Zombies/tree/main/zombie>`_

`Home Page <https://medium.com/@peterjrigali/best-weapon-in-zombies-9fddd33735c5>`_
