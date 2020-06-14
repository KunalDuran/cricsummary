# cricsummary


cricsummary is built for performing cricket analysis on data provided by cricsheet.org. 

  - Convert yaml file to csv
  - Creates Separate DataFrame for Team1 and Team2 
  - Vizualise or Perform your own transformations on the DataFrames


You can also:
  - Save the converted file (yaml to csv)
  - Plot Manhattan and Worm charts
  - Export documents as HTML(in next release)

It was created for cricket lovers to get insights from the data in an easy manner.

> This is a useful tool for performing quick cricket analysis.

### Installation

cricsummary requires python 3.5+ to run.

```
$ pip install cricsummary
```

### Development

Want to contribute? Great!

### How to Use 
```
>>> from cricsummary import Duranz
>>> match = Duranz('file.yaml')
>>> match.summary(team=1) # Summary table of team1, 2 for team2
>>> match.plot_worm() # Worm plot 
>>> match.plot_manhattan(team=2) # manhattan of team2 
```

### Do your Analysis
 - Access separate DataFrames of teams in Jupyter notebook and do your Operations/Analysis
```
df, df2 = match.team1_df, match.team2_df 
```

License
----

MIT


**Free Software, Hell Yeah!**