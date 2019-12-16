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

	def __new__(self, game_folder, all_lineups, predicted_score, mvp_probability, minSalary, lineups):
		expandedtop_df = all_lineups
		predicted_df = predicted_score
		mvp_prob_df = mvp_probability

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
#			print(mvp_player)
			num_mvps = math.floor(row['sel_count'])
#			print(num_mvps)
			mvp_temp_df = expandedtop_df.loc[expandedtop_df['MVP - 1.5X Points'] == mvp_player].copy()
			mvp_temp_df = mvp_temp_df.sort_values('Total_ManFPPG', ascending=False )
			mvp_temp_df = mvp_temp_df.iloc[0:num_mvps]
			tosubmit_df = tosubmit_df.append(mvp_temp_df, ignore_index=True)

		tosubmit_df = tosubmit_df.sort_values('Total_ManFPPG', ascending=False )
		tosubmit_df = tosubmit_df.reset_index(drop=True)		
		tosubmit_df['selection_index'] = tosubmit_df.index
		tosubmit_df['selection_type'] = "mvp_top"
#		tosubmit_df.info()

		export_csv = tosubmit_df.to_csv(os.path.join(game_folder, 'mvp_top_selection_lineups_data.csv'), index=True, header=True)
		
		headerList = []
		headerList = ["MVP - 1.5X Points","AnyFLEX","AnyFLEX","AnyFLEX","AnyFLEX"]
		submit_lineups_df = tosubmit_df[["MVP - 1.5X Points","Flex_1","Flex_2","Flex_3","Flex_4"]].copy()
		export_csv = submit_lineups_df.to_csv(os.path.join(game_folder, 'mvp_top_selection_lineups_upload.csv'), index=None, header=headerList)
		
