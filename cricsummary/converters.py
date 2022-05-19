import yaml, os, json
import pandas as pd
import numpy as np


def convert_over_to_df(over_data):
    over_df = pd.DataFrame(over_data)
    over_df['runs_by_bat']= over_df['runs'].apply(lambda x : x.get('batter'))
    over_df['extra_runs']= over_df['runs'].apply(lambda x : x.get('extras'))
    over_df['total']= over_df['runs'].apply(lambda x : x.get('total'))
    over_df['delivery'] = np.arange(1, len(over_df)+1)
    
    if 'extras'  in over_df.columns:
        over_df['extra_type'] = over_df['extras'].apply(lambda x: "".join(list(x.keys())) if type(x) == dict else np.nan)
    
    if 'wickets'  in over_df.columns:
        over_df['wicket_type'] = over_df['wickets'].apply(lambda x: x[0].get('kind') if type(x) == list else np.nan)
        over_df['player_out'] = over_df['wickets'].apply(lambda x: x[0].get('player_out')  if type(x) == list else np.nan)
        def get_fielder_name(x):
            fielder_list = x[0].get('fielders') if type(x) == list else []
            if fielder_list:
                return ';'.join(fielder.get('name') for fielder in fielder_list)
            return np.nan
        over_df['fielder'] = over_df['wickets'].apply(get_fielder_name)
        over_df.drop(columns=['wickets'], inplace=True)
        

    over_df['extra_type'] = np.nan
    over_df['wicket_type'] = np.nan
    over_df['player_out'] = np.nan
    over_df['fielder'] = np.nan
        
        
    over_df.drop(columns=['runs'], inplace=True)
    return over_df


def complete_team_df(team_overs):
    all_overs = []
    for over_index, over in enumerate(team_overs):
        over_df = convert_over_to_df(over['deliveries'])
        over_df['over'] = over_index+1
        all_overs.append(over_df)
    return pd.concat(all_overs, ignore_index=True)


def json_to_csv(match_file, output_file=False):
    
    with open(match_file, 'r') as f:
        file = json.load(f)
    
    info = file['info']
    innings = file['innings']
    length = len(innings)
    
    if length == 0:
        print('No innings data found')
        return [], info


    all_innings_df = {}
    for idx, inning in enumerate(innings):
        team = inning['overs']
        df = complete_team_df(team)
        df['extra_type'] = df['extra_type'].fillna('-')
        df['wicket_type'] = df['wicket_type'].fillna(0)

        team_innings = f"{inning['team']}_{idx+1}"
        if output_file:
            
            file_path = f"{os.path.splitext(os.path.split(match_file)[-1])[0]}_{team_innings}.csv"
            df.to_csv(file_path)
        
        all_innings_df[team_innings]=df

    return all_innings_df, info



## deprecated function
def yaml_to_csv(match_file, output_file=False):
    '''
    deprecated: function no longer supported because earlier cricsheet.org used to provide data mainly in yaml files
    but now they are providing json files also which is now primarily being used in cricsummary. 
    '''
    with open(match_file, 'r') as f:
        file = yaml.safe_load(f)
    info = file['info']
    
    innings = file['innings']
    
    length = len(innings)
    
    def organizing(team):
        structured = {}
        structured['Over_and_ball'] = [key for ball in team for key in ball]
        structured['Batsman'] = [list(ball.values())[0].get('batsman') for ball in team]
        structured['Non_striker'] = [list(ball.values())[0].get('non_striker') for ball in team]
        structured['Bowler'] = [list(ball.values())[0].get('bowler') for ball in team]
        structured['runs'] = [list(ball.values())[0].get('runs') for ball in team]
        structured['wicket'] = [list(ball.values())[0].get('wicket',0) for ball in team]
        df = pd.DataFrame(structured)
        df['Runs_off_bat'] = df.runs.apply(lambda x: x.get('batsman'))
        df['Extras'] = df.runs.apply(lambda x: x.get('extras'))
        df['Total'] = df.runs.apply(lambda x: x.get('total')).cumsum()
        df['Kind_of_wicket'] = df.wicket.apply(lambda x: x.get('kind') if x!=0 else 0)
        df['Dismissed_player'] = df.wicket.apply(lambda x: x.get('player_out') if x!=0 else 0)
        df.drop(columns=['runs', 'wicket'], inplace=True)
        from math import ceil
        df['Over'] = df['Over_and_ball'].apply(lambda x: ceil(x))
        return df

    file_path1 = f"{os.path.splitext(os.path.split(match_file)[-1])[0]}_team1.csv"
    file_path2 = f"{os.path.splitext(os.path.split(match_file)[-1])[0]}_team2.csv"
    file_path3 = f"{os.path.splitext(os.path.split(match_file)[-1])[0]}_team3.csv"
    file_path4 = f"{os.path.splitext(os.path.split(match_file)[-1])[0]}_team4.csv"
    
    if length == 0:
        print('No innings data found')
        return None, None, None, None, info
    
    elif length == 1:
        team1 = innings[0]['1st innings']['deliveries']
        team_name1 = innings[0]['1st innings']['team']
        df1 = organizing(team1).assign(Innings_number=1,team=team_name1)

        if output_file:
            df1.to_csv(file_path1)
        else:
            return df1, None, None, None, info
        
    elif length == 2:
        team_name1 = innings[0]['1st innings']['team']
        team_name2 = innings[1]['2nd innings']['team']
        team2 = innings[1]['2nd innings']['deliveries']
        team1 = innings[0]['1st innings']['deliveries']

        df1 = organizing(team1).assign(Innings_number=1,team=team_name1)
        df2 = organizing(team2).assign(Innings_number=2,team=team_name2)
    
        if output_file:
            df1.to_csv(file_path1)
            df2.to_csv(file_path2)

        else:
            return df1, df2, None, None, info

    elif length == 3:
        team_name1 = innings[0]['1st innings']['team']
        team_name2 = innings[1]['2nd innings']['team']
        team_name3 = innings[2]['3rd innings']['team']
        team3 = innings[2]['3rd innings']['deliveries']
        team2 = innings[1]['2nd innings']['deliveries']
        team1 = innings[0]['1st innings']['deliveries']

        df1 = organizing(team1).assign(Innings_number=1,team=team_name1)
        df2 = organizing(team2).assign(Innings_number=2,team=team_name2)
        df3 = organizing(team3).assign(Innings_number=3,team=team_name3)
    
        if output_file:
            df1.to_csv(file_path1)
            df2.to_csv(file_path2)
            df3.to_csv(file_path3)

        else:
            return df1, df2, df3,None, info

    elif length == 4:
        team_name1 = innings[0]['1st innings']['team']
        team_name2 = innings[1]['2nd innings']['team']
        team_name3 = innings[2]['3rd innings']['team']
        team_name4 = innings[3]['4th innings']['team']
        team4 = innings[3]['4th innings']['deliveries']
        team3 = innings[2]['3rd innings']['deliveries']
        team2 = innings[1]['2nd innings']['deliveries']
        team1 = innings[0]['1st innings']['deliveries']

        df1 = organizing(team1).assign(Innings_number=1,team=team_name1)
        df2 = organizing(team2).assign(Innings_number=2,team=team_name2)
        df3 = organizing(team3).assign(Innings_number=3,team=team_name3)
        df4 = organizing(team4).assign(Innings_number=4,team=team_name4)
    
        if output_file:
            df1.to_csv(file_path1)
            df2.to_csv(file_path2)
            df3.to_csv(file_path3)
            df4.to_csv(file_path4)

        else:
            return df1, df2, df3, df4, info
