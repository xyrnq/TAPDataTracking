# TAP session stats tracking module
# todo: Refactor tracking from controller to here

import TAPDataInterfaceHigh as TDIH

import math as maths

# death stats variables
previousFive = []
deathPB = 0
numberGames = 0
numberDeathGames = 0
numberDeathM = 0
numberDeathGM = 0
deathAverage = 0
deathMAverage = 0
totalDeathLevels = 0
totalDeathMLevels = 0
mTime = None

# master stats variables
pb = None

def update_series():
	global previousFive
	if len(previousFive) >= 5:
		previousFive.pop(0)
	
	previousFive.append(TDIH.get_level())

def get_series_total():
	return sum(previousFive)
	
# returns true if a change, false otherwise
def update_death_pb():
	global deathPB
	if TDIH.get_level() > deathPB:
		deathPB = TDIH.get_level()
		return True
	return False

def update_game_counter():
	global numberGames
	numberGames += 1
	
def update_death_games():
	global numberDeathGames
	numberDeathGames += 1

# returns true if a change, false otherwise
def update_death_m():
	global numberDeathM
	if TDIH.get_level() > 500:
		numberDeathM += 1
		return True
	return False	

# returns true if a change, false otherwise
def update_death_gm():
	global numberDeathGM
	if TDIH.get_level() == 999:
		numberDeathGM += 1
		return True
	return False
		
def update_death_average():
	global deathAverage
	deathAverage = maths.floor(totalDeathLevels / numberDeathGames)

# returns true if a change, false otherwise
def update_death_m_average():
	global deathMAverage
	if TDIH.get_level() > 500:
		deathMAverage = maths.floor(totalDeathMLevels / numberDeathM)
		return True
	return False

# returns true if a change, false otherwise
def update_m_time():
	global mTime
	# there is a slight delay because of the if statement so getting the time first
	time = TDIH.get_timer()
	if mTime == None and TDIH.get_level() > 500:
		mTime = time
		return True
		
	return False

def reset_m_time():
	global mTime
	mTime = None
	
def update_death_levels():
	global totalDeathLevels
	global totalDeathMLevels
	totalDeathLevels += TDIH.get_level()
	if TDIH.get_level() > 500:
		totalDeathMLevels += TDIH.get_level()
