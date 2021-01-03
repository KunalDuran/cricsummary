import yaml, os
import pandas as pd

def yaml_to_csv(match_file, output_file=False):
    with open(match_file, 'r') as f:
        file = yaml.safe_load(f)
    info = file['info']
    team2 = file['innings'][1]['2nd innings']['deliveries']
    team1 = file['innings'][0]['1st innings']['deliveries']
    def organizing(team):

        find_extras = lambda record: list(record.values())[0].get('extras')

        structured = {}
        structured['Over_and_ball'] = [key for ball in team for key in ball]
        structured['Batsman'] = [list(ball.values())[0].get('batsman') for ball in team]
        structured['Non_striker'] = [list(ball.values())[0].get('non_striker') for ball in team]
        structured['Bowler'] = [list(ball.values())[0].get('bowler') for ball in team]
        structured['runs'] = [list(ball.values())[0].get('runs') for ball in team]
        structured['wicket'] = [list(ball.values())[0].get('wicket',0) for ball in team]
        structured['Extra_type'] = [list(find_extras(record).keys())[0] if find_extras(record) else "-" for record in team]
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
    if output_file:
        file_path1 = f"{os.path.splitext(os.path.split(match_file)[-1])[0]}_team1.csv"
        file_path2 = f"{os.path.splitext(os.path.split(match_file)[-1])[0]}_team2.csv"

        organizing(team1).assign(Innings_number=1).to_csv(file_path1, index=False)
        organizing(team2).assign(Innings_number=2).to_csv(file_path2, index=False)
    else:
        return organizing(team1).assign(Innings_number=1), organizing(team2).assign(Innings_number=2), info
