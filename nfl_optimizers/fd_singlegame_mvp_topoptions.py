import pandas as pd
import numpy as np
from scipy import optimize
import itertools
from itertools import combinations
import os
from functools import reduce
import random
from numpy.random import choice
from collections import Counter
import math

class mvptop:

	def __init__(self, game_folder, game_file, minSalary, lineups):
		#super().__init__(game_folder, game_file)
		maxSalary = 60000
		
		teamname_df = pd.read_csv("TeamNameABVMap.csv")
		teamname_df = teamname_df.rename(columns={"Team Full Name": "Tm"})
	
		roster_file = os.path.join(game_folder, game_file)
		fd_df = pd.read_csv(roster_file)
		
		#TEAMS AND LOCATION
		game = fd_df.iloc[0]['Game']
		game = str(game.replace("@", "at"))
		
		#DROP players
#		fd_df = fd_df.head(16)
		fd_df = fd_df.loc[(fd_df['Injury Indicator'] != 'DROP')]		
		print('Number of potential roster members: {one}'.format(one=len(fd_df.index)))
		#CALCULATE MVP SCORE
		#fd_df['Actual-MVP'] = fd_df['Actual']*1.5
		fd_df['ManFPPG-MVP'] = fd_df['ManFPPG']*1.5
		fd_df['ManHi-MVP'] = fd_df['ManHi']*1.5
		fd_df['ManLo-MVP'] = fd_df['ManLo']*1.5
		
		#CALCULATE VALUE = FPPG/SALARY
		fd_df['Value'] = fd_df['FPPG']/fd_df['Salary']*1000  #calculate value = FPPG/Salary * 1000
		
		predicted_df = fd_df[['Player ID + Player Name','ManFPPG','ManFPPG-MVP','ManHi','ManHi-MVP','ManLo','ManLo-MVP']].copy()
		
		#CREATE MVP PROBABILITY DB
		mvp_prob_df = fd_df[['Player ID + Player Name','mvp_prob']].copy()
		
		fd_df['Player ID + Player Name'] = fd_df['Player ID + Player Name'].astype(str) + ','
		
		#ALL COMBINATIONS
		lineup = []
		for index in list(combinations(fd_df.index,5)):
		    lineup.append(fd_df.loc[index,['Player ID + Player Name','Salary','Opponent']].sum())
		print('Number of potential lineups: {one}'.format(one=len(lineup)))
		all_lineups_df = pd.DataFrame(np.array(lineup), columns = ['Player ID + Player Name','Salary','Opponent'])

		#REMOVE LINEUPS THAT EXCEED ALLOWED SALARY
		all_lineups_df['Salary'] = all_lineups_df['Salary'].astype(int)
		all_lineups_df = all_lineups_df.loc[all_lineups_df['Salary'] <= maxSalary]
		print('Number of potential lineups after removing high salary: {one}'.format(one=len(all_lineups_df.index)))
		
		#REMOVE LINEUPS WITH ONLY ONE TEAM
		teamlist = []
		teamlist = fd_df['Opponent'].unique()
		team1 = teamlist[0]*5
		team2 = teamlist[1]*5
		all_lineups_df = all_lineups_df.loc[(all_lineups_df['Opponent'] != team1) & (all_lineups_df['Opponent'] != team2)]
		print('Number of potential lineups after removing same team: {one}'.format(one=len(all_lineups_df.index)))
		
		#SEPERATE OUT PLAYERS OF POSSIBLE LINEUPS
		all_lineups_df['player1'] = all_lineups_df['Player ID + Player Name'].str.split(',').str[0]
		all_lineups_df['player2'] = all_lineups_df['Player ID + Player Name'].str.split(',').str[1]
		all_lineups_df['player3'] = all_lineups_df['Player ID + Player Name'].str.split(',').str[2]
		all_lineups_df['player4'] = all_lineups_df['Player ID + Player Name'].str.split(',').str[3]
		all_lineups_df['player5'] = all_lineups_df['Player ID + Player Name'].str.split(',').str[4]
		
		#SWAP OUT MVP FOR EACH POTENTIAL LINEUP
		expandtoplineup = []
		lineup2dlist = []
		for index, row in all_lineups_df.iterrows():
		    e1 = [row['player1'],row['player2'],row['player3'],row['player4'],row['player5'],row['Salary']]
		    e2 = [row['player2'],row['player1'],row['player3'],row['player4'],row['player5'],row['Salary']]
		    e3 = [row['player3'],row['player2'],row['player1'],row['player4'],row['player5'],row['Salary']]
		    e4 = [row['player4'],row['player2'],row['player3'],row['player1'],row['player5'],row['Salary']]
		    e5 = [row['player5'],row['player2'],row['player3'],row['player4'],row['player1'],row['Salary']]
		    expandtoplineup.append(e1)
		    expandtoplineup.append(e2)
		    expandtoplineup.append(e3)
		    expandtoplineup.append(e4)
		    expandtoplineup.append(e5)
		expandedtop_df = pd.DataFrame(np.array(expandtoplineup), columns = ['MVP - 1.5X Points','Flex_1','Flex_2','Flex_3','Flex_4','Salary'])
		expandedtop_df['original index'] = expandedtop_df.index
		print('Number of potential lineups with mvp swap: {one}'.format(one=len(expandedtop_df.index)))

		#FILTER LINUPS BASED ON SALARY RANGE
#		minSalary = 57000
		expandedtop_df['Salary'] = expandedtop_df['Salary'].astype(int)
		expandedtop_df = expandedtop_df.loc[expandedtop_df['Salary'] >= minSalary]
		
		#DEF CALCULATE POINTS FOR EACH POSITION WITHIN THE LINEUP AND SUM THE TOTAL
		expandedtop_df['MVP_ManFPPG'] = expandedtop_df['MVP - 1.5X Points'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG-MVP'].to_dict())
		expandedtop_df['Flex1_ManFPPG'] = expandedtop_df['Flex_1'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG'].to_dict())
		expandedtop_df['Flex2_ManFPPG'] = expandedtop_df['Flex_2'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG'].to_dict())
		expandedtop_df['Flex3_ManFPPG'] = expandedtop_df['Flex_3'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG'].to_dict())
		expandedtop_df['Flex4_ManFPPG'] = expandedtop_df['Flex_4'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG'].to_dict())
		expandedtop_df['MVP_ManHi'] = expandedtop_df['MVP - 1.5X Points'].map(predicted_df.set_index('Player ID + Player Name')['ManHi-MVP'].to_dict())
		expandedtop_df['Flex1_ManHi'] = expandedtop_df['Flex_1'].map(predicted_df.set_index('Player ID + Player Name')['ManHi'].to_dict())
		expandedtop_df['Flex2_ManHi'] = expandedtop_df['Flex_2'].map(predicted_df.set_index('Player ID + Player Name')['ManHi'].to_dict())
		expandedtop_df['Flex3_ManHi'] = expandedtop_df['Flex_3'].map(predicted_df.set_index('Player ID + Player Name')['ManHi'].to_dict())
		expandedtop_df['Flex4_ManHi'] = expandedtop_df['Flex_4'].map(predicted_df.set_index('Player ID + Player Name')['ManHi'].to_dict())
		expandedtop_df['MVP_ManLo'] = expandedtop_df['MVP - 1.5X Points'].map(predicted_df.set_index('Player ID + Player Name')['ManLo-MVP'].to_dict())
		expandedtop_df['Flex1_ManLo'] = expandedtop_df['Flex_1'].map(predicted_df.set_index('Player ID + Player Name')['ManLo'].to_dict())
		expandedtop_df['Flex2_ManLo'] = expandedtop_df['Flex_2'].map(predicted_df.set_index('Player ID + Player Name')['ManLo'].to_dict())
		expandedtop_df['Flex3_ManLo'] = expandedtop_df['Flex_3'].map(predicted_df.set_index('Player ID + Player Name')['ManLo'].to_dict())
		expandedtop_df['Flex4_ManLo'] = expandedtop_df['Flex_4'].map(predicted_df.set_index('Player ID + Player Name')['ManLo'].to_dict())
		
		manfppg_list=[]
		manfppg_list=['MVP_ManFPPG','Flex1_ManFPPG','Flex2_ManFPPG','Flex3_ManFPPG','Flex4_ManFPPG']
		manhi_list=[]
		manhi_list=['MVP_ManHi','Flex1_ManHi','Flex2_ManHi','Flex3_ManHi','Flex4_ManHi']
		manlo_list=[]
		manlo_list=['MVP_ManLo','Flex1_ManLo','Flex2_ManLo','Flex3_ManLo','Flex4_ManLo']
		
		expandedtop_df['Total_ManFPPG'] = expandedtop_df[manfppg_list].sum(axis=1)
		expandedtop_df['Total_ManHi'] = expandedtop_df[manhi_list].sum(axis=1)
		expandedtop_df['Total_ManLo'] = expandedtop_df[manlo_list].sum(axis=1)
		expandedtop_df = expandedtop_df.sort_values('Total_ManFPPG', ascending=False )
		expandedtop_df = expandedtop_df.reset_index(drop=True)
		expandedtop_df['scoring_index'] = expandedtop_df.index
		expandedtop_df['scoring_type'] = "manfppg"
				
		#convert mvp_prop to number of lineups. How many lineups * prop = lineups for each member. update mpv_prop_df with number
		mvp_prob_df['sel_count'] = mvp_prob_df['mvp_prob']*lineups
		
		tosubmit_df = pd.DataFrame()
		
		for i, row in mvp_prob_df.iterrows():
			mvp_player = row['Player ID + Player Name']
			print(mvp_player)
			num_mvps = math.floor(row['sel_count'])
			print(num_mvps)
			mvp_temp_df = expandedtop_df.loc[expandedtop_df['MVP - 1.5X Points'] == mvp_player].copy()
			mvp_temp_df = mvp_temp_df.sort_values('Total_ManFPPG', ascending=False )
			mvp_temp_df = mvp_temp_df.iloc[0:num_mvps]
			tosubmit_df = tosubmit_df.append(mvp_temp_df, ignore_index=True)

		tosubmit_df = tosubmit_df.sort_values('Total_ManFPPG', ascending=False )
		tosubmit_df = tosubmit_df.reset_index(drop=True)		
		tosubmit_df['selection_index'] = tosubmit_df.index
		tosubmit_df['selection_type'] = "mvp_top"
		tosubmit_df.info()

		export_csv = tosubmit_df.to_csv(os.path.join(game_folder, 'mvp_top_selection_lineups_data.csv'), index=True, header=True)
		
		headerList = []
		headerList = ["MVP - 1.5X Points","AnyFLEX","AnyFLEX","AnyFLEX","AnyFLEX"]
		submit_lineups_df = tosubmit_df[["MVP - 1.5X Points","Flex_1","Flex_2","Flex_3","Flex_4"]].copy()
		export_csv = submit_lineups_df.to_csv(os.path.join(game_folder, 'mvp_top_selection_lineups_upload.csv'), index=None, header=headerList)
		
