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

class actual_winnings:

	def __init__(self, game_folder, selection_file, scoring_file):
		#super().__init__(game_folder, game_file)
#		maxSalary = 60000
		
#		teamname_df = pd.read_csv("TeamNameABVMap.csv")
#		teamname_df = teamname_df.rename(columns={"Team Full Name": "Tm"})
	
		selection = os.path.join(game_folder, selection_file)
		selection_df = pd.read_csv(selection)

#		money = os.path.join(game_folder, pooch_results)
		winnings_df = pd.read_csv(scoring_file)
		
		final_df = pd.merge(selection_df, winnings_df, on='original index', how='inner', suffixes=('_selection', '_actuals'))
		final_df.info()
		
#		output_df = final_df[['MVP - 1.5X Points','Flex_1','Flex_2','Flex_3','Flex_4','Salary','original index','scoring_index','scoring_type','selection_index','selection_type','Total_Actual','actual_index','Winnings']].copy()
		
		export_csv = final_df.to_csv(os.path.join(game_folder, 'selection_winnings.csv'), index=True, header=True)
				
