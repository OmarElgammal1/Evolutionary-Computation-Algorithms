from graph import TSPGraph
import adjacency_mat_generator
from random import randint
# from manim import *


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


# class AntColonyVisualizer(Scene):
#     def __init__(self, adj_mat, n_cities, alpha=1, beta=1):
#         super().__init__()
#         self.graph = TSPGraph(adj_mat, n_cities, alpha=alpha, beta=beta)
#         self.n_cities = n_cities
#         self.nodes = [i for i in range(self.n_cities)]
#         self.edges = self.__make_edges(self.n_cities)

#     def __make_edges(self, n):
#         edges = []
#         for i in range(n):
#             for j in range(i+1, n):
#                 edges.append((i, j))
                
#         return edges
        
#     def construct(self):
#         g = Graph(self.nodes, self.edges, layout="spring", layout_scale=12,
#                   labels=True, vertex_config={'radius':0.5})

#         scene_width = 40
#         scene_height = 30
#         self.camera.frame_width = scene_width        
#         self.camera.frame_height = scene_height
#         top_center = [0, scene_height / 2, 0]

#         N_ANTS = 20
#         N_ITERS = 10
#         ant_dots = [Dot(color=ManimColor.from_hex("#FF0000")) for _ in range(N_ANTS)]
#         node_positions = {label: dot.get_center() for label, dot in g.vertices.items()}

#         best_cycle, best_cost, traversal_history = self.optimize(n_iters=N_ITERS, n_ants=N_ANTS, degradation_factor=0.8)
#         for i in range(N_ITERS):
#             iteration_number = Tex(f"Iteration {i}").set_position(top_center)
#             nth_iteration_cycles = traversal_history[i]
#             for j in range(len(nth_iteration_cycles)):
#                 jth_ant = nth_iteration_cycles[j]
#                 print(jth_ant)


#         # SRC_NODE = 0
#         # ant = Dot(color=random_color())
#         # ant = Dot(node_positions[SRC_NODE], color=RED)
#         self.play(Create(g))
#         # self.play(ant.animate.move_to(node_positions[SRC_NODE + 1]), run_time=2)
    
#     def optimize(self, n_iters, n_ants, degradation_factor=0.5, q=1, use_elitism=False):
#         traversal_history = []
#         graph_cpy = self.graph.copy()
#         best_cost = float("inf")
#         best_cycle = None
#         for _ in range(n_iters):
#             ant_cycles = [graph_cpy.traverse(randint(0, self.n_cities - 1)) for _ in range(n_ants)]
#             if use_elitism and best_cycle:
#                 ant_cycles.append((best_cycle, best_cost))
            
#             traversal_history.append(ant_cycles)

#             ant_cycles.sort(key=lambda x: x[1])
#             if use_elitism and best_cycle and ant_cycles[0][1] < best_cycle[1]:
#                 best_cycle = ant_cycles[0]
                
#             for cycle, total_cost in ant_cycles:
#                 best_cost, best_cycle = self.__update_best_cycle(cycle, total_cost, best_cycle, best_cost)
#                 self.__update_pheromone(graph_cpy, cycle, q, total_cost, degradation_factor)

#         return best_cycle, best_cost, traversal_history
    
#     def __update_pheromone(self, graph_cpy, cycle, q, total_cost, degradation_factor):
#         delta = q/total_cost
#         for i in range(len(cycle) - 1):
#             graph_cpy.adj_matrix[cycle[i], cycle[i+1], 1] += delta
        
#         graph_cpy.adj_matrix[cycle[-1], cycle[0], 1] += delta
#         graph_cpy.adj_matrix[:, :, 1] *= degradation_factor

    
#     def __update_best_cycle(self, cycle, cycle_cost, best_cycle, best_cost):
#         if cycle_cost < best_cost:
#             return cycle_cost, cycle
#         return best_cost, best_cycle
    


