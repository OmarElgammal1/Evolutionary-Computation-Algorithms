import numpy as np
import random

class TSPGraph:
    def __init__(self, adj_matrix, n_cities, alpha = 1, beta = 1) -> None:
        self.adj_matrix = np.array(adj_matrix)
        self.n_cities = n_cities
        self.alpha = alpha
        self.beta = beta

    def copy(self):
        return TSPGraph(self.adj_matrix.copy(), self.n_cities, self.alpha, self.beta)

    def traverse(self, source_index=0):
        visited = np.zeros(self.n_cities)
        visited[source_index] = 1
        # Hamiltonian cycle
        cycle = [source_index]
        # Total cost of the cycle
        total_cost = 0
        for _ in range(self.n_cities - 1):
            # const to avoid divide by zero
            epsilon = 1e-10
            # list of adjacent nodes
            adj_nodes = [i for i in range(self.n_cities) if not visited[i]]
            # pheromone intensities of adjacent nodes
            pheromone_intensities = self.adj_matrix[source_index, :, 1]
            # costs of adjacent nodes
            costs = self.adj_matrix[source_index, :, 0]
            # calculating weights of adjacent nodes
            weights = (pheromone_intensities ** self.alpha) / ((costs + epsilon) ** self.beta)
            # removing visited nodes
            weights = np.delete(weights, np.argwhere(visited == 1).flatten())
            # selecting next node
            next_node = random.choices(adj_nodes, weights)[0]
            total_cost += self.adj_matrix[source_index][next_node][0]
            visited[next_node] = 1
            source_index = next_node
            cycle.append(source_index)

        total_cost += self.adj_matrix[cycle[-1]][cycle[0]][0] # returning to source
        return cycle, total_cost

# graph = TSPGraph(4)
# print(graph.adj_matrix)
# print(graph.traverse())

