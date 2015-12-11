# ------------------------------------------- #
# File: ship_gui.py                           #
# Brief: Ship gui object file.                #
# Author: Philipp Schaad                      #
# Creation Date: 081215                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

import ship_base


# GUI-Ship object class.
class ShipGUI(ship_base.Ship):

    def add_damage(self):
        if super(ShipGUI, self).add_damage():
            # TODO Notify on sunk!
            return True
        return False
