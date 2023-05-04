from poker.classes.poker import Poker


if __name__ == '__main__':
        me = 'Peter @ Jf-Q4OmfIt'
        repo = 'C:\\Users\\Peter\\Desktop\\vscode\\poker\\data\\'
        grouped = {'Peter'   : ('mQWfGaGPXE', 'ijDyevyKYD', 'Jf-Q4OmfIt', 'hOG9_DzBzN'),
                'Flynn'   : ('YEtsj6CMK4', 'M_ODMJ-3Je', 'DZy-22KNBS', 'AAVEC4azwk', 'vbV5gsPyQT'),
                'Mike'    : ('1_FRcDzJU-', 'ofZ3AjBJdl', 'yUaYOqMtWh', 'EIxKLHzvif', 'welPeANz41'),
                'Johnny'  : ('3fuMmmzEQ-', 'LRdO6bTCRh', '9fNOKzXJkb', '88zR6gcIvD'),
                'Robby'   : ('FZayb4wOU1', '66rXA9g5yF', 'rM6qlbc77h', 'fy6-0HLhb_', 'nlk80T6XeC', 'HSzay5VpMS', 'XBGaWogyTu'),
                'Carter'  : ('48QVRRsiae', 'u8_FUbXpAz'),  # , 'y5NDFZCA3B'
                'Pfanz'   : ('Aeydg8fuEg', 'yoohsUunIZ', 'pvow8N1-FT', '6T99AA7TTd'),
                'Yuri'    : ('mUwL4cyOAC', 'zGv-6DI_aJ', 'DySJmToB8p'),
                'Brian'   : ('FgmbZrCA9u', 'K7wE-uWJaj', 'kNiVoJP5Ym', 'rsoe5Ywx7C'),
                'Henry'   : ('HiZcYKvbcw', 'GXxPFeJI6u', '59DT1gf9Cu'),
                'Kaz'     : ('e_guu9eD6Q', '4pYZ-YdlJa', 'xkNOUZ2mr1'),
                'Nate'    : ('uVSlQwPVtk', 'YDeMDTtJPl'),
                'Bryson'  : ('-qWOsSgvQM', 'HTi7AMTQNr'),
                'Jack'    : ('VnrRHVzTZy', 'twk14-WLnE'),
                'Baker'   : ('cKZ72RXCxd', 'uRb9uI6e8-'),
                'Sinclair': ('cjuTQ51KDm',),
                'Ryan'    : ('eR3DTX32e8',),
                'Robert'  : ('BSg5NL6pWI', 'itJbCfezw9'),
                }
        user_inputs = {'me': me, 'repo': repo, 'grouped': grouped, 'line_limit': 50, 'item_limit': 50}
        p = Poker(user_inputs=user_inputs)
