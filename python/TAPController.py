# file controlling both the session and all time stats

import TAPStatsSession as TSS

import TAPDataInterfaceHigh as TDIH
import TAPDataInterfaceEnums as TDIE
import TAPDataInterfaceLow as TDIL

import time

def output(string, flag = None, file = None):
	print(string)
	if file != None:
		with open(file, flag) as writeFile:
			writeFile.write(string)

def reset_all_session_files():
	with open("tappb.dat", 'w') as write_file:
		write_file.write("SB: 0; Games: 0")
	
	open("taphistory.dat", 'w')
            
	with open("tapm_count.dat", 'w') as write_file:
		write_file.write("M count: 0")
		
	with open("tapgm_count.dat", 'w') as write_file:
		write_file.write("GM count: 0")
		
	with open("tapaverage.dat", 'w') as write_file:
		write_file.write("Average:")
		
	with open("tapmaverage.dat", 'w') as write_file:
		write_file.write("M Avg:")
		
	with open("last_m_time.dat", 'w') as write_file:
		write_file.write("Last M time: ")

def main():

	time.sleep(1)
	print("Waiting until loading has finished...")
	while TDIH.get_state() != TDIE.State.idle:
		time.sleep(0.05)
	print("Loading completed")
	
	reset_all_session_files()
	
	gameProcessed = False
	
	while True:		
		if TDIH.get_mode() == TDIE.Mode.death and not gameProcessed:
			if TSS.update_m_time():
				output("Last M time: " + TSS.mTime, 'w', "last_m_time.dat")
		
		if TDIH.get_state() == TDIE.State.gameOver and not gameProcessed:
			#update the number of games played
			TSS.update_game_counter()
			
			if TDIH.get_mode() == TDIE.Mode.master:
				continue
			elif TDIH.get_mode() == TDIE.Mode.death:
				# update number of death games
				TSS.update_death_games()
				
				# update history
				TSS.update_series()
				output("Lvl: " + str(TDIH.get_level()) + "; Tot: " + str(TSS.get_series_total()) + "\n", 'a', "taphistory.dat")
				
				# update PB
				TSS.update_death_pb()
				output("SB: " + str(TSS.deathPB) + "; Games: " + str(TSS.numberDeathGames), 'w', "tappb.dat")
				
				# update number of Ms
				if TSS.update_death_m():
					output("M count: " + str(TSS.numberDeathM), 'w', "tapm_count.dat")
				
				# update number of GMs
				if TSS.update_death_gm():
					output("GM count: " + str(TSS.numberDeathGM), 'w', "tapgm_count.dat")
					
				# update death levels
				TSS.update_death_levels()
				
				# update death average
				TSS.update_death_average()
				output("Average: " + str(TSS.deathAverage), 'w', "tapaverage.dat")
				
				# update death M average
				if TSS.update_death_m_average():
					output("M Avg: " + str(TSS.deathMAverage), 'w', "tapmaverage.dat")
					
				TSS.reset_m_time()
				
				gameProcessed = True
		elif TDIL.get_timer() == 0:
			gameProcessed = False
			
		time.sleep(0.01)


if __name__ == '__main__':
    main()