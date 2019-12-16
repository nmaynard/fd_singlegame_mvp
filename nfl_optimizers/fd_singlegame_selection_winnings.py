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

class selection_winnings:

	def __init__(self, game_folder, selection_file):

		actual_selection_file = os.path.join(game_folder, selection_file)
		actual_selection_df = pd.read_csv(actual_selection_file)
		#calculate top_opt winnings
#		actual_selection_df.info()

		mvp_top_actual_df = actual_selection_df.dropna(subset=['mvp_top_index'])
#		mvp_top_actual_df.info()
		mvp_top_total = mvp_top_actual_df['Winnings'].sum()
		print('mvp_top_total: {one}'.format(one=mvp_top_total))
		result = [['mvp_top', mvp_top_total]]

		mvp_prob_actual_df = actual_selection_df.dropna(subset=['mvp_prob_index'])
#		mvp_prob_actual_df.info()
		mvp_prob_total = mvp_prob_actual_df['Winnings'].sum()
		print('mvp_prob_total: {one}'.format(one=mvp_prob_total))
		mvp_prob_result = ['mvp_prob', mvp_prob_total] 
		result.append(mvp_prob_result)
		print(result)

		sel_results_df = pd.DataFrame(result, columns = ['selection', 'winnings'])
		
		export_csv = sel_results_df.to_csv(os.path.join(game_folder, 'selection_final_results.csv'), index=False, header=True)
		