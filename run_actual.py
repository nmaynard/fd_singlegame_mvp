from nfl_optimizers.fd_singlegame_actual import single_game_actual as Actual
from nfl_optimizers.fd_singlegame_pooch_result import pooch_winnings as Winnings
#Salary Low, Num Lineups, Actual, folderPath, filePath, abvPath
lineups = Actual(game_folder = "/Users/Nate/Desktop/FanDual/fd_singlegame/01Dec2019_NEatHOU",
					game_file = "FanDuel-NFL-2019-12-01-41085-lineup-ACTUAL.csv")
					
winnings = Winnings(pooch_folder = "/Users/Nate/Desktop/FanDual/fd_singlegame/01Dec2019_NEatHOU",
					pooch_file = "FanDuel-NFL-2019-12-01-41085-lineup-ACTUAL.csv",
					pooch_rewards = "pooch_rewards.csv")

