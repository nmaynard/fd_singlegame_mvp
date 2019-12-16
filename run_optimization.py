from nfl_optimizers.fd_singlegame_lineup_creation import lineup_creation as allLineups
from nfl_optimizers.fd_singlegame_mvp_prob_selection import mvprandom as Random
from nfl_optimizers.fd_singlegame_mvp_topoptions_selection import mvptop as TopMVPs

minSalary = 50000

[all_lineups, predicted, mvp] = allLineups(game_folder = "/Users/Nate/Desktop/FanDual/fd_singlegame/01Dec2019_NEatHOU",
										game_file = "FanDuel-NFL-2019-12-01-41085-lineup-upload-template.csv")

#Salary Low, Num Lineups, Actual, folderPath, filePath, abvPath
lineups_random = Random(game_folder = "/Users/Nate/Desktop/FanDual/fd_singlegame/01Dec2019_NEatHOU",
					alllineups = all_lineups,
					predicted_score  = predicted,
					mvp_probability = mvp,
					minSalary = 50000,
					manfppg_top_slice = 2000,
					lineups = 150)
					
#Salary Low, Num Lineups, Actual, folderPath, filePath, abvPath
lineups_top = TopMVPs(game_folder = "/Users/Nate/Desktop/FanDual/fd_singlegame/01Dec2019_NEatHOU",
					alllineups = all_lineups,
					predicted_score  = predicted,
					mvp_probability = mvp,
					minSalary = 50000,
					lineups = 150)

