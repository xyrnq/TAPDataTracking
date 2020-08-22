# A module for low level interfacing with the memory mapped file
# of shmupmametgm modified by MHL. The file is located at
# %APPDATA%\taptracker_data on windows and
# /dev/shm/taptracker_data on *nix.

# At this time this only runs on Windows.

# imports used for reading the memory mapped file
import mmap
import struct

# import for getting file location
import os

# memory struct
# 0 - state
# 1 - grade
# 2 - gradePoints
# 3 - level
# 4 - timer
# 5 - tetromino
# 6 - xcoord
# 7 - ycoord
# 8 - rotation
# 9 - mrollFlags
# 10 - inCreditRoll
# 11 - gameMode
def _unpack_mmap_block(n):
    return struct.unpack("@h", _mm[n * _DATA_BLOCK_SIZE:(n+1) * _DATA_BLOCK_SIZE])[0]

# 0 -
# 1 - Spawn frame? Needs confirmation
# 2 - tetromino can be controlled by the player
# 3 - tetromino cannot be influenced anymore
# 4 - tetromino is being locked to the playfield
# 5 - in block entry delay (ARE)
# 7 - "Game Over" is being shown on screen
# 10 - no game has started, idle state. This is the state in "ready go" portion as well
# 11 - blocks are fading away when topping out (losing)
# 12 - DAS charged in ARE? Needs confirmation
# 13 - blocks are fading away when completing a game
# 71 - garbage value when the game is still loading
def get_state():
	return _unpack_mmap_block(0)
	
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
# 31+    			   | S9
####
# Can get grades in modes that aren't Master
# This is not how you get the grade in death
# The grade in death needs to be calculated from the time and level
def get_grade():
	return _unpack_mmap_block(1)

# 0 - 100, when reaching 100 grade increases by 1 then resets grade points to 0
def get_gradePoints():
	return _unpack_mmap_block(2)
	
# get the current level
# is set to the last level in the last game until either a demo
# screen is displayed, or the select mode menu is displayed.
# When the select mode menu is displayed it resets to 0
def get_level():
	return _unpack_mmap_block(3)

# this returns the number of frames since the mode has started
# to calculate seconds since mode started just multiply by 100/60
# note that the timer and game run at different frame rates
# and this calculation is for the game timer, not the wall time
def get_timer():
	return _unpack_mmap_block(4)

# 2 - I
# 3 - Z
# 4 - S
# 5 - J
# 6 - L
# 7 - O
# 8 - T
# item = piece + 8192 in normal, untested in item mode
def get_tetromino():
	return _unpack_mmap_block(5)
	
def get_xcoord():
	return _unpack_mmap_block(6)
	
def get_ycoord():
	return _unpack_mmap_block(7)
	
# 0 - spawn orientation
# 1 - ccw 90
# 2 - 180
# 3 - ccw 270 aka cw 90
def get_rotation():
	return _unpack_mmap_block(8)


# 17 - failure state in the first half of the game 100-499
# 19 - failure state in the second half of the game 500-999
# 31 - failure state at the end of the game, currently in fading credit roll
# 34 - garbage value when the game is still loading
# 48 - neutral state. Value during the first section and not playing master mode
# 49 - passing state during the first half of the game 100-499
# 51 - passing state during the second half of the game 500-999
# 127 - passing state at the end of the game, currently in the invisible credit roll
def get_mrollFlags():
	return _unpack_mmap_block(9)

# I believe this is only for the fading roll and M-roll
# Possibly works for death, but untested.
def get_inCreditRoll():
	return _unpack_mmap_block(10)

# 0 - no game mode
# 1 - normal
# 2 - master
# 4 - doubles
# 128 - tgm+
# 4096 - death
# this updates when hovering in the selection menu as well
def get_mode():
	return _unpack_mmap_block(11)
	
# the file to read is 12 blocks of 2 bytes integers	
_DATA_BLOCK_SIZE = 2
_NUMBER_OF_BLOCKS = 12
_taptrackerfile = open(os.getenv('APPDATA') + "\\taptracker_data", "r+b")
_mm = mmap.mmap(_taptrackerfile.fileno(), _DATA_BLOCK_SIZE * _NUMBER_OF_BLOCKS)
