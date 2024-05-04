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


def random_adjacency_mat(n_cities):
    # making a matrix where each edge has [cost, pheromone_intensity]
    tuples = np.array([(np.random.randint(3, 51), 1)
                        for i in range(n_cities ** 2)])
    graph = tuples.reshape(n_cities, n_cities, 2)

    # setting diagonal to zeros
    indices = np.diag_indices(n_cities)
    graph[indices] = [0, 0]
    return graph