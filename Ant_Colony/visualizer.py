import adjacency_mat_generator
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from ant_colony import AntColonyOptimization
from manim import *
import numpy as np

class AntColonyVisualizer(Scene):
    def __init__(self):
        super().__init__()
        self.N_CITIES = 4
        self.N_ANTS = 2
        self.N_ITERS = 2
        self.ADJ_MAT = adjacency_mat_generator.adjacency_matrix_test1()

        self.ant_colony_optimizer = AntColonyOptimization(self.ADJ_MAT, self.N_CITIES, alpha=1, beta=1)
        self.n_cities = self.N_CITIES
        self.nodes = [i for i in range(self.n_cities)]
        self.edges = self.__make_edges(self.n_cities)

    def __make_edges(self, n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                edges.append((i, j))
                
        return edges
    
    def __make_pheromones_intensities_edge_map(self, adj_matrix):
        edge_phero = {}
        for i in range(self.n_cities):
            for j in range(i+1, self.n_cities):
                edge_phero[(i, j)] = adj_matrix[i][j]
        
        return edge_phero
    
    def __setup_camera(self, width, height):
        self.camera.frame_width = width        
        self.camera.frame_height = height

    def __populate_ant_moves(self, ant_moves, traversal_history, node_positions):
        for i in range(self.N_ITERS):
            nth_iteration_cycles = traversal_history[i]
            for j in range(len(nth_iteration_cycles)):
                jth_ant = nth_iteration_cycles[j]
                cycle = jth_ant[0]
                
                for k in range(len(cycle)):
                    ant_moves[i][k].append(node_positions[cycle[k]])
                ant_moves[i][-1].append(node_positions[cycle[0]])
    
    def __populate_edge_label_animation(self, edge_labels, graph_lines, edge_phero, edge_animations):
        for txt, e in zip(edge_labels, self.edges):
                line = graph_lines[e]
                line_direction = line.get_end() - line.get_start()
                offset = 1.0 * (line_direction / np.linalg.norm(line_direction))
                phero = str(round(edge_phero[e], 2))
                edge_animations.append(txt.animate.become(Tex(phero)).move_to(line.get_start() + offset).set_z_index(10))

    def __get_edge_colors(self, edge_pheromone_val):
        color = interpolate_color(BLUE, GREEN, edge_pheromone_val).to_rgb() # the greater the phero intensity the closer it is to green
        color[0] = 0 # make red = 0
        color[1] -= 0.1 # color less green
        color[2] += 0.1 # make blue bluer
        return color

    def __populate_edge_recolor_animations(self, graph_lines, edge_phero, edge_recolor):
        for edge in self.edges:
                line = graph_lines[edge]
                line_phero_val = float(edge_phero[edge]) * 10.0
                color = self.__get_edge_colors(line_phero_val)
                edge_recolor.append(line.animate.set_color(ManimColor.from_rgb(color)).set_stroke(width=(line_phero_val*20 + 10)))

    def construct(self):
        g = Graph(self.nodes, self.edges, layout="spring", layout_scale=12,
                  labels=True, vertex_config={'radius':0.5})
        self.__setup_camera(40, 30)
        top_center = [-15, 14, 0]

        
        ant_dots = [Dot(color=ManimColor.from_hex("#FF0000")).scale(2).set_z_index(10) for _ in range(self.N_ANTS)]
        self.add(*ant_dots)

        ant_moves = [[[] for _ in range(self.n_cities + 1)] for _ in range(self.N_ITERS)] # each iteration has n movements = n_cities (for each cycle)
        iteration_text = Tex(f"Iteration 0")

        node_positions = {label: dot.get_center() for label, dot in g.vertices.items()}
        best_cycle, best_cost = self.ant_colony_optimizer.optimize(n_iters=self.N_ITERS, n_ants=self.N_ANTS, degradation_factor=0.1)
        edge_phero = self.__make_pheromones_intensities_edge_map(self.ant_colony_optimizer.intensity_history[0])

        graph_lines = g.edges # (i, j): Line object -------> where i, j are vertices
        edge_labels = [Tex().set_z_index(10) for _ in range(len(self.edges))]
        edge_animations = []
        self.__populate_edge_label_animation(edge_labels, graph_lines, edge_phero, edge_animations)
        self.__populate_ant_moves(ant_moves, self.ant_colony_optimizer.traversal_history, node_positions)
            
        edge_recolor = [graph_lines[edge].animate.set_color(ManimColor.from_rgb((0.0, 0.2, 1.0))).set_stroke(width=10) for edge in self.edges]
        self.play(Create(g), edge_animations, edge_recolor, runtime=3)
        
        for i in range(0, self.N_ITERS):
            edge_phero = self.__make_pheromones_intensities_edge_map(self.ant_colony_optimizer.intensity_history[i + 1])
            self.play(iteration_text.animate.become(Tex(f"Iteration {i}")).move_to(top_center), runtime=2)
            for j in range(self.n_cities + 1):
                next_ant_positions = ant_moves[i][j]
                moves = [ant_dots[k].animate.move_to(next_ant_positions[k]) for k in range(self.N_ANTS)]
                self.play(moves, runtime=1)

            # Reset dots
            remove_dots = [FadeOut(ant_dots[k]) for k in range(self.N_ANTS)]
            ant_dots = [Dot(color=ManimColor.from_hex("#FF0000")).scale(2).set_z_index(10) for _ in range(self.N_ANTS)]
            create_dots = [Create(ant_dots[k]) for k in range(self.N_ANTS)]
            self.play(remove_dots, create_dots, runtime=3)
            
            self.wait(0.5)
            # Update edges
            edge_recolor = []
            self.__populate_edge_recolor_animations(graph_lines, edge_phero, edge_recolor)
            edge_animations = []
            self.__populate_edge_label_animation(edge_labels, graph_lines, edge_phero, edge_animations)
            
            # animate edges
            self.play(edge_recolor, edge_animations, runtime=2)

        # TODO: Make everything disappear (fade in/fade out) and display best path
        # TODO: write cost on edges of best cycle