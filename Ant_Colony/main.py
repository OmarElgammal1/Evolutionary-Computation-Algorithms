import adjacency_mat_generator
from ant_colony import AntColonyOptimization

# demo for ant colony optimization
def demo(n_cities, n_ants):
    adj_mat = adjacency_mat_generator.random_adjacency_mat(n_cities, 12)
    aco = AntColonyOptimization(adj_mat, n_cities)
    for i in n_ants:
        best_cycle, best_cost = aco.optimize(50, i)
        print(f'Best cycle: {best_cycle}, Best cost: {best_cost}')


# demo for ant colony optimization with 10 cities
demo(10,[1,5,10,20])

# demo for ant colony optimization with 20 cities
demo(20,[1,5,10,20])
