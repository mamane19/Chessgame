# Author: Modester_Bello_Group
# -*- coding: utf-8 -*-
"""
Main file of the pychecs2 package. It is this file that we will run to start your game.

"""
from pychecs2.echecs.game import Game
from pychecs2.interface.interface import Window



if __name__ == '__main__':
    # Create a new Game
    p = Game()

    # Creation and display of a window (no link with the part above).
    f = Window()
    f.mainloop()
