from nfl_optimizers.fd_singlegame_lineup_creation import lineup_creation as allLineups
from nfl_optimizers.fd_singlegame_mvp_prob_selection import mvprandom as Random
from nfl_optimizers.fd_singlegame_mvp_topoptions_selection import mvptop as TopMVPs


game_folder = "/Users/Nate/Desktop/FanDual/fd_singlegame/15Dec2019_BUFatPIT"
game_file = "FanDuel-NFL-2019-12-15-41552-lineup-upload-template.csv"
minSalary = 50000
manfppg_top_slice = 2000
lineups = 150

#Create Potential Lineups
[all_lineups, predicted_score, mvp_probability] = allLineups(game_folder, game_file)

lineups_random = Random(game_folder, all_lineups, predicted_score, mvp_probability, minSalary, manfppg_top_slice, lineups)
					
lineups_top = TopMVPs(game_folder, all_lineups, predicted_score, mvp_probability, minSalary, lineups)

