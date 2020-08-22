# A module of enums storing the constants used by TAP

import enum

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
class State(enum.Enum):
	null0 = 0
	null1 = 1
	tetrominoControllable = 2 
	tetrominoNonControllable = 3
	tetrominoLocking = 4
	inARE = 5
	gameOver = 7
	idle = 10
	fadingBlocksLose = 11
	DASChargedARE = 12
	fadingBlocksComplete = 13
	garbageValue = 71
	
	# apparently you can get a state 6
	@classmethod
	def _missing_(cls, value):
		return None

# 2 - I
# 3 - Z
# 4 - S
# 5 - J
# 6 - L
# 7 - O
# 8 - T
# item = piece + 8192 in normal, untested in item mode
class Tetromino(enum.Enum):
	I = 2
	Z = 3
	S = 4
	J = 5
	L = 6
	O = 7
	T = 8
	Iitem = 8194
	Zitem = 8195
	Sitem = 8196
	Jitem = 8197
	Litem = 8198
	Oitem = 8199
	Titem = 8200

# 0 - spawn orientation
# 1 - ccw 90
# 2 - 180
# 3 - ccw 270 aka cw 90
class rotation(enum.Enum):
	spawn = 0
	ccw90 = 1
	ccw180 = 2
	ccw270 = 3

# 17 - failure state in the first half of the game 100-499
# 19 - failure state in the second half of the game 500-999
# 31 - failure state at the end of the game, currently in fading credit roll
# 34 - garbage value when the game is still loading
# 48 - neutral state. Value during the first section and not playing master mode
# 49 - passing state during the first half of the game 100-499
# 51 - passing state during the second half of the game 500-999
# 127 - passing state at the end of the game, currently in the invisible credit roll
class MRollFlags(enum.Enum):
	failedFirstHalf = 17
	failedSecondHalf = 19
	currentlyFadingRoll = 31
	garbageValue = 34
	neutralState = 48
	passingFirstHalf = 49
	passingSecondHalf = 51
	currentlyInvisibleRoll = 127
	
# 0 - no game mode
# 1 - normal
# 2 - master
# 4 - doubles
# 128 - tgm+
# 4096 - death
# this updates when hovering in the selection menu as well
####
#todo Update the enum to support all modes from codes
####
class Mode(enum.Enum):
	noMode = 0
	normal = 1
	master = 2
	doubles = 4
	tgmPlus = 128
	death = 4096
	masterVS = 10

	# haven't added all the modes values yet and
	# there is a weird interaction after selecting
	# either death or TGM+ with the selection next time
	@classmethod
	def _missing_(cls, value):
		return None
