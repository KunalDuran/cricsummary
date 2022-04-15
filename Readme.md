# cricsummary


cricsummary is built for performing cricket analysis on data provided by cricsheet.org. 
by converting the data in DataFrames or csv files that are better suited for analysis. 

  - Convert json file to csv.
  - Creates DataFrames team-wise. 
  - Vizualise or Perform your own transformations/analysis on the DataFrames.
  - Save the converted file (json to csv)
  - Plot Manhattan and Worm charts



> This is a useful tool to get started with cricket analysis.

### Installation

cricsummary requires python 3.5+ to run.

```
$ pip install cricsummary
```



### How to Use 
Download the data from cricsheet 
Use the txt file in downloaded folder to check name of the match you want to analyse
```
>>> from cricsummary import Duranz


>>> match = Duranz('12345.json')


### BUILT IN METHODS FOR ANAYSIS

# team parameter represent innings, team=1 for data of team batted in 1st inning 
>>> match.scorecard(team=1) 

>>> match.plot_worm() 

>>> match.plot_manhattan(team=2)

>>> match.match_info()

>>> match.extras(team=1)

>>> match.fall_of_wickets(team=2)
```

### Do your Analysis
 - Access separate DataFrames of teams and do your Operations/Analysis
```
# returns dict of dataframe where keys are team name with _<innings> suffix 
match = Duranz('123.json')
>>> df_dict = match.teams_df

### CONVERT JSON TO CSV 
>>> from cricsummary import json_to_csv

# this will save the files of the innings <teamname>_<innings>.csv
>>> json_to_csv('123.json', output_file=True)

```


### Development

Want to contribute? Great!
pull request on https://github.com/KunalDuran/cricsummary

License
----

MIT

