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
        self.N_CITIES = 10
        self.N_ANTS = 50
        self.N_ITERS = 50
        self.ADJ_MAT = adjacency_mat_generator.random_adjacency_mat(10, 12)

        self.ant_colony_optimizer = AntColonyOptimization(self.ADJ_MAT, self.N_CITIES, alpha=1, beta=1)
        self.n_cities = self.N_CITIES
        self.nodes = [i for i in range(self.n_cities)]
        self.edges = self.__make_edges(self.n_cities)

    def construct(self):
        g = Graph(self.nodes, self.edges, layout="spring", layout_scale=12,
                  labels=True, vertex_config={'radius':0.5})
        self.__setup_camera(40, 30)
        self.camera.background_color = ManimColor.from_hex("#1B1F42")

        top_center = [-17, 10, 0]

        
        ant_dots = [Dot(color=ManimColor.from_hex("#FF0000")).scale(3).set_z_index(10) for _ in range(self.N_ANTS)]
        self.add(*ant_dots)

        ant_moves = [[[] for _ in range(self.n_cities + 1)] for _ in range(self.N_ITERS)] # each iteration has n movements = n_cities (for each cycle)
        iteration_text = Tex(f"Iteration 0")

        node_positions = {label: dot.get_center() for label, dot in g.vertices.items()}
        best_cycle, best_cost = self.ant_colony_optimizer.optimize(n_iters=self.N_ITERS, n_ants=self.N_ANTS, degradation_factor=0.1)
        edge_phero = self.__make_pheromones_intensities_edge_map(self.ant_colony_optimizer.intensity_history[0])

        graph_lines = g.edges # (i, j): Line object -------> where i, j are vertices
        edge_labels = {edge: Tex().set_z_index(10) for edge in self.edges}
        edge_animations = []
        self.__populate_edge_label_animation(edge_labels.values(), graph_lines, edge_phero, edge_animations)
        self.__populate_ant_moves(ant_moves, self.ant_colony_optimizer.traversal_history, node_positions)
            
        edge_recolor = [graph_lines[edge].animate.set_color(ManimColor.from_rgb((1.0, 1.0, 1.0))).set_stroke(width=10) for edge in self.edges]
        self.play(Create(g), edge_animations, edge_recolor, runtime=3)
        
        for i in range(0, self.N_ITERS):
            edge_phero = self.__make_pheromones_intensities_edge_map(self.ant_colony_optimizer.intensity_history[i + 1])
            self.play(iteration_text.animate.become(Tex(f"Iteration {i}", font_size=82)).move_to(top_center), runtime=2)
            for j in range(self.n_cities + 1):
                next_ant_positions = ant_moves[i][j]
                moves = [ant_dots[k].animate.move_to(next_ant_positions[k]) for k in range(self.N_ANTS)]
                self.play(moves, runtime=1)

            # Reset dots
            remove_dots = [FadeOut(ant_dots[k]) for k in range(self.N_ANTS)]
            ant_dots = [Dot(color=ManimColor.from_hex("#FF0000")).scale(3).set_z_index(10) for _ in range(self.N_ANTS)]
            create_dots = [Create(ant_dots[k]) for k in range(self.N_ANTS)]
            if i == self.N_ITERS - 1:
                self.play(remove_dots, runtime=3)
            else:
                self.play(remove_dots, create_dots, runtime=3)

            self.wait(0.5)
            # Update edges
            edge_recolor = []
            self.__populate_edge_recolor_animations(graph_lines, edge_phero, edge_recolor)
            edge_animations = []
            self.__populate_edge_label_animation(edge_labels.values(), graph_lines, edge_phero, edge_animations)
            
            # animate edges
            self.play(edge_recolor, edge_animations, runtime=2)
        
        self.wait(1)
        # visualize best cycle
        best_cycle_text = iteration_text.animate.become(Tex('Best Cycle', font_size=82)).move_to(top_center)
        src_node = best_cycle[0]
        dest_node = best_cycle[-1]

        # recolor src node
        src_color = [g.vertices[src_node].animate.set_color(RED_C), g.vertices[src_node].submobjects[0].animate.set_color(WHITE)]
        dest_color = [g.vertices[dest_node].animate.set_color(RED_C), g.vertices[dest_node].submobjects[0].animate.set_color(WHITE)]
        # print(g.vertices[src_node].submobjects)
        ant = Dot(node_positions[src_node], color=ManimColor.from_hex("#000000")).scale(2).set_z_index(10)

        # drop non used edges
        non_used_edges = self.__get_non_used_edges(best_cycle)
        for edge in non_used_edges:
            self.play(FadeOut(graph_lines[edge]), FadeOut(edge_labels[edge]))
        
        # setup best cycle animations
        return_edge = (dest_node, src_node)
        if return_edge not in graph_lines:
            return_edge = (src_node, dest_node)
        
        non_used_edges = set(non_used_edges)
        cost_display = []
        costs = []
        best_cost_pos = (top_center[0], top_center[1]-2, top_center[2])
        best_cost_number_pos = (top_center[0]+3, top_center[1]-2, top_center[2])

        for edge in self.edges:
            if edge not in non_used_edges or edge == return_edge:
                line = graph_lines[edge]
                cost = str(int(self.ADJ_MAT[edge[0], edge[1], 0]))
                costs.append(int(cost))

                line_direction = line.get_end() - line.get_start()
                offset = 2.0 * (line_direction / np.linalg.norm(line_direction))

                position = line.get_start() + offset
                cost_display.append(edge_labels[edge].animate.become(Text(cost, weight=BOLD).move_to(position).set_z_index(10).scale(1.5).set_color(ManimColor.from_hex("#BBBBBB"))))


        best_cost_text = Tex('')
        best_cost_animation = best_cost_text.animate.become(Tex(f'Best Cost =', font_size=82)).move_to(best_cost_pos) ###########
        best_cost_number = Integer(0)
        
        return_edge_animation = FadeIn(graph_lines[return_edge].set_color(RED))
        self.play(best_cost_animation, Create(best_cost_number.move_to(best_cost_number_pos)), cost_display, best_cycle_text, src_color, dest_color, return_edge_animation, Create(ant), runtime=6)

        # best_cost_number.next_to(lambda d: d.next_to(best_cost_text, RIGHT))

        # animate best cycle
        for i in range(len(best_cycle) - 1):
            start = best_cycle[i]
            end = best_cycle[i + 1]

            new_best_cost = int(self.ADJ_MAT[start, end, 0])
            update_cost = best_cost_number.animate.increment_value(new_best_cost).move_to(best_cost_number_pos)
            self.play(update_cost, ant.animate.move_to(node_positions[best_cycle[i + 1]]))

        return_edge_cost = int(self.ADJ_MAT[best_cycle[0], best_cycle[-1], 0])
        self.play(best_cost_number.animate.increment_value(return_edge_cost).move_to(best_cost_number_pos), ant.animate.move_to(node_positions[best_cycle[0]]))
        self.play(FadeOut(ant))
    
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
                offset = 2.0 * (line_direction / np.linalg.norm(line_direction))
                phero = str(round(edge_phero[e], 2))
                edge_animations.append(txt.animate.become(Text(phero, weight=BOLD)).move_to(line.get_start() + offset).scale(1.1).set_z_index(10).set_color(ManimColor.from_hex("#BBBBBB")))

    def __get_edge_colors(self, edge_pheromone_val):
        # color = interpolate_color(BLUE, GREEN, edge_pheromone_val).to_rgb() # the greater the phero intensity the closer it is to green
        color = interpolate_color(YELLOW, ORANGE, edge_pheromone_val).to_rgb() # the greater the phero intensity the closer it is to Orange
        color[0] += 0.08 # increase red
        # color[1] -= 0.1 # color less green
        # color[2] -= 0.2 # make blue bluer
        return color
    
    def __populate_edge_recolor_animations(self, graph_lines, edge_phero, edge_recolor):
        max_phero = max(edge_phero.values())
        for edge in self.edges:
                line = graph_lines[edge]
                line_phero_val = float(edge_phero[edge]) * 10.0
                color = self.__get_edge_colors(line_phero_val)
                edge_recolor.append(line.animate.set_color(ManimColor.from_rgb(color)).set_stroke(width=(line_phero_val*20 + 10)))

    def __get_non_used_edges(self, cycle):
        used_edges = set()
        for i in range(1, len(cycle)):
            used_edges.add((cycle[i-1], cycle[i]))

        non_used_edges = []
        for edge in self.edges:
            reversed_edge = (edge[1], edge[0])
            if edge not in used_edges and reversed_edge not in used_edges:
                non_used_edges.append(edge)

        return non_used_edges
    
        # TODO: Make everything disappear (fade in/fade out) and display best path
        # TODO: write cost on edges of best cycle