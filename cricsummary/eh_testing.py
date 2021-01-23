import cricsummary
path = "C:/Users/Ewan/OneDrive/Python Projects/Cricket Database/tests/64124.yaml"

match = cricsummary.Duranz(path)

# print(match.team1_df)
# print(match.team2_df)
# print(match.team3_df)
# print(match.team4_df)

match.plot_worm()