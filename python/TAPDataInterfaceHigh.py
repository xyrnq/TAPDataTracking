# A module for high level interfacing with the memory mapped file
# of shmupmametgm modified by MHL. The file is located at
# %APPDATA%\taptracker_data on windows and
# /dev/shm/taptracker_data on *nix.

# At this time this only runs on Windows.

import TAPDataInterfaceLow as TDIL
import TAPDataInterfaceEnums as TDIE

import math as maths

# 0 -
# 1 - 
# 2 - tetromino can be controlled by the player
# 3 - tetromino cannot be influenced anymore
# 4 - tetromino is being locked to the playfield
# 5 - block entry delay (ARE)
# 7 - "Game Over" is being shown on screen
# 10 - no game has started, idle state. This is the state in "ready go" portion as well
# 11 - blocks are fading away when topping out (losing)
# 13 - blocks are fading away when completing a game
# 71 - garbage value when the game is still loading
#
# See the file TAPDataInterfaceEnums for enum values
def get_state():
	return TDIE.State(TDIL.get_state())

# returns a string that is the displayed grade
# Internal grade value | Displayed grade
# 0     			   | 9
# 1     			   | 8
# 2    				   | 7
# 3    				   | 6
# 4  				   | 5
# 5-6 				   | 4
# 7-8  				   | 3
# 9-11 				   | 2
# 12-14 			   | 1
# 15-17 			   | S1
# 18   				   | S2
# 19    			   | S3
# 20-22 			   | S4
# 23-24 			   | S5
# 25-26 			   | S6
# 27-28 			   | S7
# 29-30 			   | S8
# 31+				   | S9
####
# Can get grades in modes that aren't Master
# This is not how you get the grade in death
# The grade in death needs to be calculated from the time and level
####
# there must be a better way to do this
####
def get_grade():
	if get_mode() == TDIE.Mode.master:
		switcher = {
			0: "9",
			1: "8",
			2: "7",
			3: "6",
			4: "5",
			5: "4",
			6: "4",
			7: "3",
			8: "3",
			9: "2",
			10: "2",
			11: "2",
			12: "1",
			13: "1",
			14: "1",
			15: "S1",
			16: "S1",
			17: "S1",
			18: "S2",
			19: "S3",
			20: "S4",
			21: "S4",
			22: "S4",
			23: "S5",
			24: "S5",
			25: "S6",
			26: "S6",
			27: "S7",
			28: "S7",
			29: "S8",
			30: "S8",
		}
		return switcher.get(TDIL.get_grade(), "S9")
	elif get_mode() == TDIE.Mode.death:
		if get_level() < 500:
			return None
		elif get_level() < 999:
			return "M"
		else:
			return "GM"
	else:
		return None
	
# 0 - 100, when reaching 100 grade increases by 1 then resets grade points to 0
def get_gradePoints():
	return TDIL.get_gradePoints()

# get the current level
# is set to the last level in the last game until either a demo
# screen is displayed, or the select mode menu is displayed.
# When the select mode menu is displayed it resets to 0
def get_level():
	return TDIL.get_level()

# converts the low level timer which is number of frames since
# the mode has started to seconds that have elapsed according
# to the game timer. This differs to wall time
def get_timer_in_seconds():
	return maths.floor(100 * TDIL.get_timer() / 60) / 100

# get the number of minutes rounded down since the mode has 
# started
def get_minutes():
	return maths.floor(get_timer_in_seconds() / 60)

# get how many seconds into this minute we are
# this gets messy if we don't do this due to rounding error
def get_seconds():
	return round(100 * (get_timer_in_seconds() - 60 * get_minutes())) / 100
	
# returns a string that is should be close to the game timer
# in testing it seems like there can be some small errors
# this can be fixed by a look up table I suspect.
# I also suspect I don't want to do that.
def get_timer():
	return str(get_minutes()) + ":" + "{:.2f}".format(get_seconds()).replace(".", ":")

# 2 - I
# 3 - Z
# 4 - S
# 5 - J
# 6 - L
# 7 - O
# 8 - T
# item = piece + 8192 in normal, untested in item mode
#
# See the file TAPDataInterfaceEnums for enum values
def get_tetromino():
	return TDIE.Tetromino(TDIL.get_tetromino())
	
def get_xcoord():
	return TDIL.get_xcoord()

def get_ycoord():
	return TDIL.get_ycoord()

# 0 - spawn orientation
# 1 - ccw 90
# 2 - 180
# 3 - ccw 270 aka cw 90
#
# See the file TAPDataInterfaceEnums for enum values
def get_rotation():
	return TDIL.get_rotation()

# 17 - failure state in the first half of the game 100-499
# 19 - failure state in the second half of the game 500-999
# 31 - failure state at the end of the game, currently in fading credit roll
# 34 - garbage value when the game is still loading
# 48 - neutral state. Value during the first section and not playing master mode
# 49 - passing state during the first half of the game 100-499
# 51 - passing state during the second half of the game 500-999
# 127 - passing state at the end of the game, currently in the invisible credit roll
#
# See the file TAPDataInterfaceEnums for enum values
def get_mrollFlags():
	return TDIE.MRollFlags(TDIL.get_mrollFlags())

# I believe this is only for the fading roll and M-roll
# Possibly works for death, but untested.
def get_inCreditRoll():
	return TDIL.get_inCreditRoll()

# 0 - no game mode
# 1 - normal
# 2 - master
# 4 - doubles
# 128 - tgm+
# 4096 - death
# this updates when hovering in the selection menu as well
#
# See the file TAPDataInterfaceEnums for enum values
def get_mode():
	return TDIE.Mode(TDIL.get_mode())

# returns the current section
def get_section():
	return maths.floor(TDIL.get_level() / 100) + 1
