.. _Intro:

*****
Intro
*****
.. meta::
   :description: Landing page for poker-now-analysis.
   :keywords: Poker, Python, Analysis, Texas Hold'em

This is a package for analyzing past performance and player habits from the Poker Now website.

=====
Usage
=====
In progress...

.. code-block:: python

    import poker
    from poker.poker_class import Poker

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


=========
More Info
=========
In progress...

