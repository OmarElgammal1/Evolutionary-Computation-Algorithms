import pandas as pd
import adjacency_mat_generator
from ant_colony import AntColonyOptimization
import os
from collections import defaultdict

data = defaultdict(list)
n_ants_trials = [1, 5, 10, 20, 50]
q_param_trials = [1, 5, 10, 15, 20]
# alpha_trials = [0.1, 0.3, 0.5, 0.8, 1]
# beta_trials = [0.1, 0.3, 0.5, 0.8, 1]
degradation_factor_trials = [0.1, 0.3, 0.5, 0.9, 1]
n_iterations = [1, 5, 10, 50, 100]
UPDATE_DEMO = False



if UPDATE_DEMO or 'demo.csv' not in os.listdir():
    for n_ants in n_ants_trials:
        for q_param in q_param_trials:
            # for alpha in alpha_trials:
            #     for beta in beta_trials:
                    for n_iteration in n_iterations:
                        for degradation_factor in degradation_factor_trials:
                            data['Number of Ants'].append(n_ants)
                            data['Q'].append(q_param)
                            # data['Alpha'].append(alpha)
                            # data['Beta'].append(beta)
                            data['Number of Iterations'].append(n_iteration)
                            data['Degradation Factor'].append(degradation_factor)
                            aco = AntColonyOptimization(adjacency_mat_generator.adjacency_matrix_test1(), 4)
                            data['Cost'].append(aco.optimize(n_iters= n_iteration, n_ants=n_ants, degradation_factor=degradation_factor, q=q_param)[1])

    df = pd.DataFrame(data)
    df.to_csv('demo.csv')
