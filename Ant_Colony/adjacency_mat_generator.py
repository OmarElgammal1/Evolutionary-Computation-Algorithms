import numpy as np

def adjacency_matrix_test1():
    return np.array([[[0, 0],
        [25, 1],
        [10, 1],
        [15, 1]
    ],
    [[25, 1],
        [0, 0],
        [10, 1],
        [45,1]
    ],
    [[10, 1],
        [10, 1],
        [0, 0],
        [5, 1]],
    [[15, 1],
        [45, 1],
        [5, 1],
        [0, 0]
        ]], dtype=np.float32)

def adjacency_matrix_test2():
    return np.array([[[0, 0],
        [2, 1],
        [1, 1],
        [1, 1],
        [1, 1]
    ],
    [[2, 1],
        [0, 0],
        [2, 1],
        [1, 1],
        [1, 1]
    ],
    [[1, 1],
        [2, 1],
        [0, 0],
        [1, 1],
        [2, 1]],
    [[1, 1],
        [1, 1],
        [1, 1],
        [0, 0],
        [2, 1]
        ],
        [
            [1, 1], [1, 1], [2, 1], [2, 1], [0, 0]
        ]], dtype=np.float32)


def random_adjacency_mat(n_cities, seed):
    # making a matrix where each edge has [cost, pheromone_intensity]
    np.random.seed(seed)
    graph = np.zeros((n_cities, n_cities, 2))
    for i in range(n_cities):
        for j in range(i, n_cities):
            if i == j:
                continue
            cost_pheromone = [np.random.randint(3, 51), 1]
            graph[i, j] = cost_pheromone
            graph[j, i] = cost_pheromone
    return graph