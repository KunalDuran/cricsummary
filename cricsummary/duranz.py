import pandas as pd 
import warnings
from .Viz import Vizuals
from .converters import  json_to_csv

warnings.filterwarnings("ignore")


class Duranz(Vizuals):

    def __init__(self, match):
        self.match = match
        if match.endswith('.json'):
            self.teams_df, self.info = json_to_csv(match)
        else:
            print('enter a valid json file')


    def get_teamdf(self, n):
        for team_inn in self.teams_df:
            if team_inn.endswith(str(n)):
                return self.teams_df[team_inn]


    def scorecard(self, team=1):
        team = self.get_teamdf(team)

        batsman_score = team.groupby('batter')['runs_by_bat'].sum()
        extras_played = [x for x in ['-', 'legbyes', 'byes', 'noballs'] if team['extra_type'].isin([x]).any()]
        balls_played = team.groupby('batter').count()['over']
        # balls_played = team.groupby(['extra_type','batter']).count().loc[extras_played].sum(level='batter')['over']


        def batting_order(df):
            openers = list(df.iloc[0][['batter','non_striker']].values)
            all_players = openers.copy()
            for player in df['batter']:
                if player not in all_players: all_players.append(player)
            return all_players


        def boundaries(df):
            boundary = df.groupby(['runs_by_bat','batter']).count()
            fours = boundary.loc[4].iloc[:,0].to_frame("4's")
            sixes = boundary.loc[6].iloc[:,0].to_frame("6's") if 6 in boundary.index else pd.DataFrame({'batter': [], "6's":[]})
            boundaries_df = fours.merge(sixes, how='outer', on='batter')
            return boundaries_df


        def wicket(df):
            result = df.query('wicket_type != 0')[['batter','wicket_type', 'fielder', 'bowler']]
            return result
        
        
        temp_result = pd.DataFrame([batsman_score, balls_played,(batsman_score/balls_played)*100], index=['runs', 'balls','SR']).T.reindex(batting_order(team))
        
        result = temp_result.merge(wicket(team),how='outer', on='batter').fillna('-')
        result = result.merge(boundaries(team), how='outer', on='batter').fillna(0)
        result = result[['batter','wicket_type', 'fielder', 'bowler','runs', 'balls', "4's" ,"6's",'SR']]
        result[["4's","6's"]] = result[["4's","6's"]].astype(int)
        return result


    def match_info(self):
        result = self.info['outcome']
        by = list(*result['by'].items())
        outcome = f"{result['winner']} Won by {by[1]} {by[0]}"
        teams_playing = "{} vs {}".format(self.info['teams'][0], self.info['teams'][1])
        match_infos = {
            'toss' : f"{self.info['toss']['winner']} won the toss and decided to {self.info['toss']['decision']} first.",
            'outcome' : outcome,
            'heading' : teams_playing
        }
        return match_infos 


    def fall_of_wicket(self, team=1):
        df = self.get_teamdf(team)
        df['running_total'] = df['total'].cumsum()
        fow = df[df['wicket_type']!=0]
        fow = zip(fow['running_total'], range(1,len(fow['running_total'])+1))
        return "FOW: "+" ".join([f"{runs}-{wicket}" for runs, wicket in fow])


    def extras(self, team=1):
        df = self.get_teamdf(team)
        return f"Extras: {df['extra_runs'].sum()}"
