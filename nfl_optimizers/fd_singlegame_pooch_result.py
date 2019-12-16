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

	def __init__(self, pooch_folder, pooch_file, pooch_rewards):
		roster_file = os.path.join(pooch_folder, pooch_file)
		actual_df = pd.read_csv(roster_file)
		actual_df.info()

		winnings_df = pd.read_csv(pooch_rewards)
		winnings_df.info()
												
		for j, row2 in actual_df.iterrows():
			#print(row2['actual_index'])
			idx = row2['actual_index']+1
#			print('index: {one}'.format(one=idx))
			for i, row in winnings_df.iterrows():
#				print('between lower: {one} and upper: {two} wins: {three}'.format(one=row['lower'],two=row['upper'], three=row['winnings']))
				if ((row['lower'] <= idx) & (row['upper'] >= idx)):
					win = row['winnings']
#					print('winnings: {one}'.format(one=win))
			actual_df.loc[j, 'Winnings'] = win
		
		export_csv = actual_df.to_csv(os.path.join(pooch_folder, 'pooch_results.csv'), index=None, header=True)

#	def convert_winnings(self, actual_index, pooch_rewards):
#
#		winnings_df = pd.read_csv(pooch_rewards)
#		winnings_df.info()
		
#		for i, row in winnings_df.iterrows():
#			print('lower: {one} and upper: {two}'.format(one=row['lower'],two=row['upper']))
#			if ((row['lower'] <= actual_index) & (row['upper'] >= actual_index)):
#				return (row['winnings'])
#				print('winnings: {one}'.format(one=row['winnings']))
#			else:
#				return(0)
		
