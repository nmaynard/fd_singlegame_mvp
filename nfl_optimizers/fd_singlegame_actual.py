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

class single_game_actual:

	def __init__(self, game_folder, game_file):
		#super().__init__(game_folder, game_file)
		maxSalary = 60000
		
		teamname_df = pd.read_csv("TeamNameABVMap.csv")
		teamname_df = teamname_df.rename(columns={"Team Full Name": "Tm"})
	
		roster_file = os.path.join(game_folder, game_file)
		fd_df = pd.read_csv(roster_file)
		
		#TEAMS AND LOCATION
		game = fd_df.iloc[0]['Game']
		game = str(game.replace("@", "at"))

		#DROP PLAYERS
#		fd_df = fd_df.head(12)
		fd_df = fd_df.loc[(fd_df['Injury Indicator'] != 'DROP')]		
		print('Number of potential roster members: {one}'.format(one=len(fd_df.index)))

		#CALCULATE MVP SCORE
		#fd_df['Actual-MVP'] = fd_df['Actual']*1.5
		fd_df['ManFPPG-MVP'] = fd_df['ManFPPG']*1.5
		fd_df['Actual-MVP'] = fd_df['Actual']*1.5
		
		#CALCULATE VALUE = FPPG/SALARY
		fd_df['Value'] = fd_df['FPPG']/fd_df['Salary']*1000  #calculate value = FPPG/Salary * 1000
		
		predicted_df = fd_df[['Player ID + Player Name','ManFPPG','ManFPPG-MVP','Actual','Actual-MVP']].copy()
		
		#CREATE MVP PROBABILITY DB
		mvp_prob_df = fd_df[['Player ID + Player Name','mvp_prob']].copy()
		
		fd_df['Player ID + Player Name'] = fd_df['Player ID + Player Name'].astype(str) + ','
		
		#ALL COMBINATIONS
		lineup = []
		for index in list(combinations(fd_df.index,5)):
		    lineup.append(fd_df.loc[index,['Player ID + Player Name','Salary','Opponent']].sum())
		print('Number of potential lineups: {one}'.format(one=len(lineup)))
		all_lineups_df = pd.DataFrame(np.array(lineup), columns = ['Player ID + Player Name','Salary','Opponent'])
		
		#REMOVE LINEUPS THAT EXCEED MAXSALARY
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
		
		#DEF CALCULATE POINTS FOR EACH POSITION WITHIN THE LINEUP AND SUM THE TOTAL
		expandedtop_df['MVP_ManFPPG'] = expandedtop_df['MVP - 1.5X Points'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG-MVP'].to_dict())
		expandedtop_df['Flex1_ManFPPG'] = expandedtop_df['Flex_1'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG'].to_dict())
		expandedtop_df['Flex2_ManFPPG'] = expandedtop_df['Flex_2'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG'].to_dict())
		expandedtop_df['Flex3_ManFPPG'] = expandedtop_df['Flex_3'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG'].to_dict())
		expandedtop_df['Flex4_ManFPPG'] = expandedtop_df['Flex_4'].map(predicted_df.set_index('Player ID + Player Name')['ManFPPG'].to_dict())
		expandedtop_df['MVP_Actual'] = expandedtop_df['MVP - 1.5X Points'].map(predicted_df.set_index('Player ID + Player Name')['Actual-MVP'].to_dict())
		expandedtop_df['Flex1_Actual'] = expandedtop_df['Flex_1'].map(predicted_df.set_index('Player ID + Player Name')['Actual'].to_dict())
		expandedtop_df['Flex2_Actual'] = expandedtop_df['Flex_2'].map(predicted_df.set_index('Player ID + Player Name')['Actual'].to_dict())
		expandedtop_df['Flex3_Actual'] = expandedtop_df['Flex_3'].map(predicted_df.set_index('Player ID + Player Name')['Actual'].to_dict())
		expandedtop_df['Flex4_Actual'] = expandedtop_df['Flex_4'].map(predicted_df.set_index('Player ID + Player Name')['Actual'].to_dict())
		
		manfppg_list=[]
		manfppg_list=['MVP_ManFPPG','Flex1_ManFPPG','Flex2_ManFPPG','Flex3_ManFPPG','Flex4_ManFPPG']
		actual_list=[]
		actual_list=['MVP_Actual','Flex1_Actual','Flex2_Actual','Flex3_Actual','Flex4_Actual']
		
		expandedtop_df['Total_ManFPPG'] = expandedtop_df[manfppg_list].sum(axis=1)
		expandedtop_df = expandedtop_df.sort_values('Total_ManFPPG', ascending=False )
		expandedtop_df = expandedtop_df.reset_index(drop=True)
		expandedtop_df['predicted_index'] = expandedtop_df.index
		expandedtop_df['Total_Actual'] = expandedtop_df[actual_list].sum(axis=1)
		expandedtop_df = expandedtop_df.sort_values('Total_Actual', ascending=False )
		expandedtop_df = expandedtop_df.reset_index(drop=True)
		expandedtop_df['actual_index'] = expandedtop_df.index		

		#DEF SLICE TOP LINEUPS FOR MVP BASED PROB SELECTION
#		manfppg_top_slice = 2000
#		pick_lineups_df = expandedtop_df.copy()
#		tosubmit_df = pick_lineups_df.iloc[0:manfppg_top_slice]
#		tosubmit_df.dropna(inplace=True)
		
		#ASSIGN PROBABILTIY FOR EACH LINEUP
#		mvpcounts = tosubmit_df['MVP - 1.5X Points'].tolist()
#		mvpfreq = Counter(mvpcounts)
#		mvp_prob_df['Frequency'] = mvp_prob_df['Player ID + Player Name'].map(mvpfreq)
#		mvp_prob_df['sel_prob'] = mvp_prob_df['mvp_prob']/mvp_prob_df['Frequency']
#		tosubmit_df['selection_prob'] = tosubmit_df['MVP - 1.5X Points'].map(mvp_prob_df.set_index('Player ID + Player Name')['sel_prob'].to_dict())
		
		#SELECT LINEUPS FROM SLICE BASED ON MVP PROBABILITIES
#		lineups = 150
#		selection = tosubmit_df['original index']
#		probability = tosubmit_df['selection_prob']
#		probability /= probability.sum()
		
#		draw = choice(selection, lineups,
#		              p=probability,replace=False)
		
#		mvps_df = tosubmit_df[tosubmit_df['original index'].isin(draw)]
		
		#CHECK MVP COUNTS ON THE SELECTION
#		mvplist = mvps_df['MVP - 1.5X Points'].tolist()
#		Counter(mvplist)
#		print(mvplist)
		
		export_csv = expandedtop_df.to_csv(os.path.join(game_folder, 'actual_results.csv'), index=True, header=True)
		
#		headerList = []
#		headerList = ["MVP - 1.5X Points","AnyFLEX","AnyFLEX","AnyFLEX","AnyFLEX"]
#		submit_lineups_df = mvps_df[["MVP - 1.5X Points","Flex_1","Flex_2","Flex_3","Flex_4"]].copy()
#		export_csv = submit_lineups_df.to_csv(os.path.join(game_folder, 'lineups_to_submit.csv'), index=None, header=headerList)
		
