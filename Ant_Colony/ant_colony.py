from graph import TSPGraph
import adjacency_mat_generator
from random import randint

class AntColonyOptimization:
    def __init__(self, adj_mat, n_cities, alpha=1, beta=1):
        self.graph = TSPGraph(adj_mat, n_cities, alpha=alpha, beta=beta)
        self.n_cities = n_cities

    # try to modify degradation factor
    def optimize(self, n_iters, n_ants, degradation_factor=0.5, q=1):
        graph_cpy = self.graph.copy()
        best_cost = float("inf")
        best_cycle = None
        for _ in range(n_iters):
            ant_cycles = [graph_cpy.traverse(randint(0, self.n_cities - 1)) for _ in range(n_ants)]
            ant_cycles.sort(key=lambda x: x[1])

            for cycle, total_cost in ant_cycles:
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_cycle = cycle

                delta = q/total_cost
                # self.graph[:, :, 1] *= degradation_factor # TODO: TRY THIS 
                
                for i in range(len(cycle) - 1):
                    graph_cpy.adj_matrix[cycle[i], cycle[i+1], 1] += delta
                
                graph_cpy.adj_matrix[cycle[-1], cycle[0], 1] += delta
                graph_cpy.adj_matrix[:, :, 1] *= degradation_factor
            # self.graph[:, :, 1] *= degradation_factor # TODO: TRY THIS
        return best_cycle, best_cost
    
    def optimize_elitism(self, n_iters, n_ants, degradation_factor):
        pass

    def optimize_maxmin(self, n_iters, n_ants, degradation_factor):
        pass

    # we will determine parameters later
    def __update_pheromone(self):
        pass


# n_ants_trials = [1, 5, 10, 20, 50]
# q_param_trials = [1, 5, 10, 15, 20]
# alpha_trials = [0.1, 0.3, 0.5, 0.8, 1]
# beta_trials = [0.1, 0.3, 0.5, 0.8, 1]
# degradation_factor_trials = [0.1, 0.3, 0.5, 0.9, 1]

# for n_ants in n_ants_trials:
#     for q_param in q_param_trials:
#         for alpha in alpha_trials:
#             for beta in beta_trials:
#                 for degradation_factor in degradation_factor_trials:
#                     pass

n_mistakes: int = 0
aco = AntColonyOptimization(adjacency_mat_generator.adjacency_matrix_test2(), 5)
for _ in range(50):
    best_cycle = aco.optimize(n_iters=30, n_ants=10)
    if best_cycle[1] != 5:
        n_mistakes += 1
    print(best_cycle)


print(f"the ants failed {n_mistakes} times")