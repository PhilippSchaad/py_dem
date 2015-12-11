# ------------------------------------------- #
# File: ship_cons.py                          #
# Brief: Ship console object file.            #
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


# Console-Ship object class.
class ShipCons(ship_base.Ship):

    def add_damage(self):
        if super(ShipCons, self).add_damage():
            print("Player ", self.owner.player_id, "'s ",
                  self.name, " has been sunk!", sep="")
            return True
        return False
