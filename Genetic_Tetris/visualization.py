import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import numpy as np

def train_plots(chromosome1_data, chromosome2_data):
    # Extract data for plotting
    scores1 = chromosome1_data['scores']
    turns1 = chromosome1_data['number_of_turns']
    scores2 = chromosome2_data['scores']
    turns2 = chromosome2_data['number_of_turns']

    # Create x-axis with indices starting from 1
    X = [i for i in range(1, len(scores1) + 1)]
    # Create the first plot (scores)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))  # Adjust figsize as needed

    # locator = FixedLocator(X)
    # for ax in fig.get_axes():
    #     ax.xaxis.set_major_locator(locator)
    # Plot scores
    lines1 = sns.lineplot(x=X, y=scores1, label='1st Chromosome', color='blue', ax=ax1)
    lines2 = sns.lineplot(x=X, y=scores2, label='2nd Chromosome', color='red', ax=ax1)
    ax1.set_xlabel('Number of Generation')
    ax1.set_ylabel('Scores')
    ax1.set_title('Scores')
    ax1.legend(loc='upper left')

    # Create the second plot (number of turns)
    lines1 = sns.lineplot(x=X, y=turns1, label='1st Chromosome', color='blue', ax=ax2)
    lines2 = sns.lineplot(x=X, y=turns2, label='2nd Chromosome', color='red', ax=ax2)
    ax2.set_xlabel('Number of Generation')
    ax2.set_ylabel('Number of Turns')
    ax2.set_title('Number of Turns')
    ax2.legend(loc='upper left')

    # Create the third plot (score/number of turns)
    lines1 = sns.lineplot(x=X, y=np.divide(scores1, turns1), label='1st Chromosome', color='blue', ax=ax3)
    lines2 = sns.lineplot(x=X, y=np.divide(scores2, turns2), label='2nd Chromosome', color='red', ax=ax3)
    ax3.set_xlabel('Number of Generation')
    ax3.set_ylabel('Score / Number of Turns')
    ax3.set_title('Score/Number of Turns')
    ax3.legend(loc='upper left')

    # Adjust layout (optional)
    plt.tight_layout()

    # Show the plots
    plt.show()

# c1 = {'scores': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5], 'number_of_turns': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]}
# c2 = {'scores': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5], 'number_of_turns': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]}

# train_plots(c1, c2)
