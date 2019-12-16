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

	def __init__(self, game_folder, actual_file, all_lineups_file):
		
		lineups_file = os.path.join(game_folder, all_lineups_file)
		lineups_actual_df = pd.read_csv(lineups_file)
		
		players_actual_df = pd.read_csv(os.path.join(game_folder, actual_file))

		players_actual_df['Actual-MVP'] = players_actual_df['Actual']*1.5

		lineups_actual_df['MVP_Actual'] = lineups_actual_df['MVP - 1.5X Points'].map(players_actual_df.set_index('Player ID + Player Name')['Actual-MVP'].to_dict())
		lineups_actual_df['Flex1_Actual'] = lineups_actual_df['Flex_1'].map(players_actual_df.set_index('Player ID + Player Name')['Actual'].to_dict())
		lineups_actual_df['Flex2_Actual'] = lineups_actual_df['Flex_2'].map(players_actual_df.set_index('Player ID + Player Name')['Actual'].to_dict())
		lineups_actual_df['Flex3_Actual'] = lineups_actual_df['Flex_3'].map(players_actual_df.set_index('Player ID + Player Name')['Actual'].to_dict())
		lineups_actual_df['Flex4_Actual'] = lineups_actual_df['Flex_4'].map(players_actual_df.set_index('Player ID + Player Name')['Actual'].to_dict())
		
		manfppg_list=[]
		manfppg_list=['MVP_ManFPPG','Flex1_ManFPPG','Flex2_ManFPPG','Flex3_ManFPPG','Flex4_ManFPPG']
		actual_list=[]
		actual_list=['MVP_Actual','Flex1_Actual','Flex2_Actual','Flex3_Actual','Flex4_Actual']
		
#		expandedtop_df['Total_ManFPPG'] = expandedtop_df[manfppg_list].sum(axis=1)
#		expandedtop_df = expandedtop_df.sort_values('Total_ManFPPG', ascending=False )
#		expandedtop_df = expandedtop_df.reset_index(drop=True)
#		expandedtop_df['predicted_index'] = expandedtop_df.index
		lineups_actual_df['Total_Actual'] = lineups_actual_df[actual_list].sum(axis=1)
		lineups_actual_df = lineups_actual_df.sort_values('Total_Actual', ascending=False )
		lineups_actual_df = lineups_actual_df.reset_index(drop=True)
		lineups_actual_df['actual_index'] = lineups_actual_df.index
		
		export_csv = lineups_actual_df.to_csv(os.path.join(game_folder, 'actual_results.csv'), index=False, header=True)
		
