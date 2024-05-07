from graph import TSPGraph
import adjacency_mat_generator
from random import randint
from manim import *

class AntColonyOptimization:
    def __init__(self, adj_mat, n_cities, alpha=1, beta=1):
        self.graph = TSPGraph(adj_mat, n_cities, alpha=alpha, beta=beta)
        self.n_cities = n_cities

    def optimize(self, n_iters, n_ants, degradation_factor=0.5, q=1, use_elitism=False):
        graph_cpy = self.graph.copy()
        best_cost = float("inf")
        best_cycle = None
        for i in range(n_iters):
            ant_cycles = [graph_cpy.traverse(randint(0, self.n_cities - 1)) for _ in range(n_ants)]
            if use_elitism and best_cycle:
                ant_cycles.append((best_cycle, best_cost))
            if not (i % 20):
                print(ant_cycles)
            ant_cycles.sort(key=lambda x: x[1])
            if use_elitism and best_cycle and ant_cycles[0][1] < best_cycle[1]:
                best_cycle = ant_cycles[0]
                
            graph_cpy.adj_matrix[:, :, 1] *= degradation_factor
            for cycle, total_cost in ant_cycles:
                best_cost, best_cycle = self.__update_best_cycle(cycle, total_cost, best_cycle, best_cost)
                self.__update_pheromone(graph_cpy, cycle, q, total_cost)
            # graph_cpy.adj_matrix[:, :, 1] *= degradation_factor

        return best_cycle, best_cost
    
    def __update_pheromone(self, graph_cpy, cycle, q, total_cost):
        delta = q/total_cost
        for i in range(len(cycle) - 1):
            graph_cpy.adj_matrix[cycle[i], cycle[i+1], 1] += delta
        
        graph_cpy.adj_matrix[cycle[-1], cycle[0], 1] += delta

    
    def __update_best_cycle(self, cycle, cycle_cost, best_cycle, best_cost):
        if cycle_cost < best_cost:
            return cycle_cost, cycle
        return best_cost, best_cycle
