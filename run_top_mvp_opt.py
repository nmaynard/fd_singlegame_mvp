from nfl_optimizers.fd_singlegame_mvp_topoptions import mvptop as TopMVPs

#Salary Low, Num Lineups, Actual, folderPath, filePath, abvPath
lineups = TopMVPs(game_folder = "/Users/Nate/Desktop/FanDual/fd_singlegame/05Dec2019_DALatCHI",
					game_file = "FanDuel-NFL-2019-12-05-41200-lineup-upload-template.csv",
					minSalary = 55000,
					lineups = 150)
					
