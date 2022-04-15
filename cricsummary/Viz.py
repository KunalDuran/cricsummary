import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



class Vizuals:
    def plot_manhattan(self, team=1):
        team_df = self.get_teamdf(team)
        plt.style.use('ggplot')
        plt.figure(figsize=(15,9))
        ass = team_df.groupby('over').sum()
        sns.barplot(x=ass.index, y=ass['total'])
        plt.show()


    def plot_worm(self):

        frames = []
        labels = []

        for inn in self.teams_df:
            frames.append(self.teams_df[inn])
            labels.append(inn)

        plt.style.use('ggplot')
        plt.figure(figsize=(12,7))

        max_over = 1

        for f,l in zip(frames,labels):
            if f is not None:
                ass = f.groupby('over').sum()
                plt.plot(ass.index, ass[['total', 'extra_runs']].sum(axis=1).cumsum(), label=l)
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
        
