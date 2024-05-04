import numpy as np
import random

class TSPGraph:
    def __init__(self, n_cities, alpha = 1, beta = 1) -> None:
        self.graph = self.generate_random_graph(n_cities)
        self.n_cities = n_cities
        self.alpha = alpha
        self.beta = beta

    def generate_random_graph(self, n_cities) -> np.ndarray:
        # making a matrix where each edge has [cost, pheromone_intensity]
        tuples = np.array([(np.random.randint(3, 51), 1)
                          for i in range(n_cities ** 2)])
        graph = tuples.reshape(n_cities, n_cities, 2)

        # setting diagonal to zeros
        indices = np.diag_indices(n_cities)
        graph[indices] = [0, 0]
        return graph

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
            pheromone_intensities = self.graph[source_index, :, 1]
            # costs of adjacent nodes
            costs = self.graph[source_index, :, 0]
            # calculating weights of adjacent nodes
            weights = (pheromone_intensities ** self.alpha) / ((costs + epsilon) ** self.beta)
            # removing visited nodes
            weights = np.delete(weights, np.argwhere(visited == 1).flatten())
            # selecting next node
            next_node = random.choices(adj_nodes, weights)[0]
            total_cost += self.graph[source_index][next_node][0]
            visited[next_node] = 1
            source_index = next_node
            cycle.append(source_index)

        return cycle, total_cost

graph = TSPGraph(10)
print(graph.graph)
print(graph.traverse())

