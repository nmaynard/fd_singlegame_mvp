from nfl_optimizers.fd_singlegame_lineup_creation import lineup_creation as allLineups
from nfl_optimizers.fd_singlegame_mvp_prob_selection import mvprandom as Random
from nfl_optimizers.fd_singlegame_mvp_topoptions_selection import mvptop as TopMVPs
from nfl_optimizers.fd_singlegame_actual_score import single_game_actual as Actual
from nfl_optimizers.fd_singlegame_all_lineup_winnings import pooch_winnings as actualWinnings
from nfl_optimizers.fd_singlegame_selection_winnings import selection_winnings as selectionWinnings

game_folder = "/Users/Nate/Desktop/FanDual/fd_singlegame/08Dec2019_SEAatLAR"
game_file = "FanDuel-NFL-2019-12-08-41357-lineup-upload-template.csv"
actual_file = "FanDuel-NFL-2019-12-08-41357-lineup-ACTUAL.csv"
all_lineups_file = "all_potential_lineups.csv"
actual_results_file = "actual_results.csv"
scoring_file = "pooch_winnings_full.csv"
mvp_top = "mvp_top_selection_lineups_data.csv"
mvp_prob = "mvp_prob_selection_lineups_data.csv"
selection_file = "acutal_winnings_results.csv"

minSalary = 50000
manfppg_top_slice = 2000
lineups = 150
winning_lineups = 32035

#Create Potential Lineups
#[all_lineups, predicted_score, mvp_probability] = allLineups(game_folder, game_file)

#lineups_random = Random(game_folder, all_lineups, predicted_score, mvp_probability, minSalary, manfppg_top_slice, lineups)
					
#lineups_top = TopMVPs(game_folder, all_lineups, predicted_score, mvp_probability, minSalary, lineups)

#actual = Actual(game_folder, actual_file, all_lineups_file)

#take all_potential_lineups.csv and ...ACTUAL.csv and assign new column called Actual Score
#Sort by actual score and then assingn winnings "winnings" to all_potential_lineups
#Add selection columns for mvp_top and mvp_prob to all_potential_lineups
#result = actualWinnings(game_folder, actual_results_file, scoring_file, mvp_top, mvp_prob)

#drop na values for selection index and sum winnings. Use later to optimize on.
selection_results = selectionWinnings(game_folder, selection_file)



