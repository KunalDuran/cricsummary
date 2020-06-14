import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



class Vizuals:
    def plot_manhattan(self, team=1):
        if team == 1: team = self.team1_df
        else: team = self.team2_df
        plt.style.use('ggplot')
        plt.figure(figsize=(15,9))
        ass = team.groupby('Over').sum()
        ax = sns.barplot(x=ass.index, y=ass['Runs_off_bat'])
        plt.show()


    def plot_worm(self, df=None, df2=None):
        df, df2 =  self.team1_df, self.team2_df
        ass = df.groupby('Over').sum()
        ass2 = df2.groupby('Over').sum()
        plt.style.use('ggplot')
        plt.figure(figsize=(12,7))
        plt.plot(ass.index, ass[['Runs_off_bat', 'Extras']].sum(axis=1).cumsum(), label='team1')
        plt.plot(ass2.index, ass2[['Runs_off_bat', 'Extras']].sum(axis=1).cumsum(), label='team2')
        plt.legend()
        plt.title('Worm', fontsize=26)
        plt.xlabel('Innings Runs',fontsize=16)
        plt.xticks(np.arange(1, max(max(ass.index), max(ass2.index)))+1)
        plt.ylabel('Overs',fontsize=16)
        plt.show()
        
