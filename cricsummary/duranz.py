import pandas as pd 
import plotly.graph_objects as go
import warnings
from .Viz import Vizuals
from .convert_yaml_to_csv import yaml_to_csv

warnings.filterwarnings("ignore")


class Duranz(Vizuals):

    def __init__(self, match):
        self.match = match
        if match.endswith('.yaml'):
            self.team1_df, self.team2_df, self.info = yaml_to_csv(match)
        else:
            columns =   ['ball',
            'Innings_number', 'Over_and_ball',
            'Batting team name',
            'Batsman',
            'Non_striker',
            'Bowler',
            'Runs_off_bat',
            'Extras',
            'Kind_of_wicket',
            'Dismissed_player']


            self.df = pd.read_csv(self.match, skiprows=21, header= None,names=columns)
            self.df.drop(columns=['ball'], inplace=True)
            self.df.fillna(0, inplace=True)


            from math import ceil
            self.df['Over'] = self.df['Over_and_ball'].apply(lambda x: ceil(x))


            self.team1_df = self.df[self.df['Innings_number'] == 1]
            self.team2_df = self.df[self.df['Innings_number'] == 2]
            self.team1_df['Total'] = self.team1_df.loc[:,['Runs_off_bat','Extras']].sum(axis=1).cumsum()
            self.team2_df['Total'] = self.team2_df.loc[:,['Runs_off_bat','Extras']].sum(axis=1).cumsum()


    def summary(self, team=1, info=True, plotly=False):
        if team == 1: team = self.team1_df
        else: team = self.team2_df
        batsman_score = team.groupby('Batsman')['Runs_off_bat'].sum()
        balls_played = team.groupby('Batsman')['Runs_off_bat'].count()

        def match_info():
            result = self.info['outcome']
            by = list(*result['by'].items())
            outcome = f"{result['winner']} Won by {by[1]} {by[0]}"
            teams_playing = "{} vs {}".format(self.info['teams'][0], self.info['teams'][1])
            return "{}\n\n{}".format(teams_playing, outcome) 
        
        def batting_order(df):
            openers = list(df.iloc[0][['Batsman','Non_striker']].values)
            all_players = openers.copy()
            for player in df.Batsman:
                if player not in all_players: all_players.append(player)
            return all_players

        def boundaries(df):
            boundary = df.groupby(['Runs_off_bat','Batsman']).count()
            fours = boundary.loc[4].iloc[:,0].to_frame("4's")
            sixes = boundary.loc[6].iloc[:,0].to_frame("6's")
            boundaries_df = fours.merge(sixes, how='outer', on='Batsman')
            return boundaries_df

        def fall_of_wicket(df):
            fow = df[df['Kind_of_wicket']!=0]
            fow = zip(fow.Total, range(1,len(fow.Total)+1))
            return "FOW: "+" ".join([f"{runs}-{wicket}" for runs, wicket in fow])

        def extras(df):
            return f"Extras: {df['Extras'].sum()}"

        def wicket(df):
            return df.query('Kind_of_wicket != 0')[['Batsman','Kind_of_wicket', 'Bowler']]
        
        def plot_ly(df):
            fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
            cells=dict(values=[df[x] for x in list(df.columns)],
                   fill_color='lavender',
                   align='left'))])
            fig.show()
        
        temp_result = pd.DataFrame([batsman_score, balls_played], index=['Runs', 'Balls']).T.reindex(batting_order(team))
        result = temp_result.merge(wicket(team),how='outer', on='Batsman').fillna('-')
        result = result.join(boundaries(team), how='outer', on='Batsman').fillna(0)
        result = result[['Batsman','Kind_of_wicket', 'Bowler', "4's" ,"6's", 'Runs', 'Balls']]
        result[["4's","6's"]] = result[["4's","6's"]].astype(int)
    
        if plotly: return plot_ly(result)
            
        return print(match_info() if self.match.endswith('yaml') else "", result, fall_of_wicket(team), extras(team), sep="\n\n") if info else result


























