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

class pooch_winnings:

	def __init__(self, game_folder, actual_results_file, scoring_file, mvp_top, mvp_prob):

		actual_file = os.path.join(game_folder, actual_results_file)
		actual_df = pd.read_csv(actual_file)

		scoring_df = pd.read_csv(scoring_file)
												
		actual_df['Winnings'] = actual_df['actual_index'].map(scoring_df.set_index((scoring_df['rank']-1))['winnings'].to_dict())

		mvp_top_file = os.path.join(game_folder, mvp_top)
		mvp_top_df = pd.read_csv(mvp_top_file)
		actual_df['mvp_top_index'] = actual_df['original index'].map(mvp_top_df.set_index(mvp_top_df['original index'])['selection_index'].to_dict())

		mvp_prob_file = os.path.join(game_folder, mvp_prob)
		mvp_prob_df = pd.read_csv(mvp_prob_file)
		actual_df['mvp_prob_index'] = actual_df['original index'].map(mvp_prob_df.set_index(mvp_prob_df['original index'])['selection_index'].to_dict())
				
		export_csv = actual_df.to_csv(os.path.join(game_folder, 'acutal_winnings_results.csv'), index=None, header=True)

