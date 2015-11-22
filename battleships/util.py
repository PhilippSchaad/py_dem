# ------------------------------------------- #
# File: util.py                               #
# Brief: Utility functions.                   #
# Author: Philipp Schaad                      #
# Creation Date: 201115                       #
# ------------------------------------------- #

# ------------------------------------------- #
# Copyright:                                  #
# This software is released under the GNU     #
# General Public License (GNU GPL). See the   #
# LICENSE.txt file for more information.      #
# ------------------------------------------- #

from time import sleep


# Clear the console output py printing 500 new lines.
def clear_output():
    for _ in range(500):
        print("")


# Helper function. Quickly pause the game for n seconds.
def pause(n):
    for i in range(n):
        print("Next Turn in", n - i, "seconds.")
        sleep(1)
