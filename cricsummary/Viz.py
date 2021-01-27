import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



class Vizuals:
    def plot_manhattan(self, team=1):
        if team == 1: team = self.team1_df
        elif team == 2: team = self.team2_df
        elif team == 3: team = self.team3_df
        else: team = self.team4_df
        plt.style.use('ggplot')
        plt.figure(figsize=(15,9))
        ass = team.groupby('Over').sum()
        ax = sns.barplot(x=ass.index, y=ass['Runs_off_bat'])
        plt.show()


    def plot_worm(self, df=None, df2=None, df3=None, df4=None):
        df, df2, df3, df4 =  self.team1_df, self.team2_df, self.team3_df, self.team4_df

        frames = [df, df2, df3, df4]
        labels = ['team1','team2','team3','team4']

        plt.style.use('ggplot')
        plt.figure(figsize=(12,7))

        max_over = 1

        for f,l in zip(frames,labels):
            if f is not None:
                ass = f.groupby('Over').sum()
                plt.plot(ass.index, ass[['Runs_off_bat', 'Extras']].sum(axis=1).cumsum(), label=l)
                max_over = max(max_over, max(ass.index))

        if max_over > 50:
            step = 10

        else:
            step = 1

        plt.legend()
        plt.title('Worm', fontsize=26)
        plt.xlabel('Overs',fontsize=16)
        plt.xticks(np.arange(1, max_over+1, step=step))
        plt.ylabel('Innings Runs',fontsize=16)
        plt.show()
        
