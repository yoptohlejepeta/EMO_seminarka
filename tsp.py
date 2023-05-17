import numpy as np
import random
import plotly.express as px


def distance(citya, cityb, cities, adj_matrix):
    return adj_matrix[cities.index(citya), cities.index(cityb)]


def f(paths, cities, adj_matrix):
    return [
        sum(
            [
                distance(path[i], path[(i + 1) % len(path)], cities, adj_matrix)
                for i in range(len(path))
            ]
        )
        for path in paths
    ]


def select(fit_values, n_parents):
    cumsum = np.cumsum(fit_values / sum(fit_values))
    selected = []
    while len(selected) < n_parents:
        r = random.random()
        for i in cumsum:
            if i > r:
                selected.append(np.where(cumsum == i)[0][0])
                break
    return selected


def crossover(n_paths, selected, paths):
    next_gen = []
    while len(next_gen) < n_paths:
        parents = random.sample(selected, 2)
        parent1, parent2 = paths[parents[0]], paths[parents[1]]
        child = [None for i in range(len(parent1))]

        length = random.randint(0, len(parent1))
        start = random.randint(0, len(parent1) - length)
        child[start : start + length] = parent1[start : start + length]

        parent2_index = 0
        for i in range(len(child)):
            while child[i] is None:
                if parent2[parent2_index] in child:
                    parent2_index += 1
                else:
                    child[i] = parent2[parent2_index]
                    parent2_index += 1

        next_gen.append(child)

    return next_gen


def mutate(paths, mutation_rate):
    for path in paths:
        if random.random() < mutation_rate:
            swap = random.sample(range(len(path)), 2)
            path[swap[0]], path[swap[1]] = path[swap[1]], path[swap[0]]
    return paths


def tsp_gen(n_paths, n_parents, cities, adj_matrix, n_gens, mutation_rate=0.1):
    gens = []
    paths = np.array([np.random.permutation(cities) for i in range(n_paths)])
    min_distance = np.inf
    best_path = None

    for gen in range(1, n_gens + 1):
        fit_values = f(paths, cities, adj_matrix)
        selected = select(fit_values, n_parents)
        paths = crossover(n_paths, selected, paths)
        paths = mutate(paths, mutation_rate)

        current_min = np.min(fit_values)
        if current_min < min_distance:
            min_distance = current_min
            best_path = paths[np.argmin(fit_values)]
        gens.append((gen, min_distance))
        print(f"Generace {gen}: Fitness = {min_distance}")

    return best_path, min_distance, gens


if __name__ == "__main__":
    cities = [
        "Chabarovice",
        "Usti nad Labem",
        "Praha",
        "Brno",
        "Karlovy Vary",
        "Kladno",
        "Ml. Boleslav",
        "Vsetaty",
    ]
    adj_matrix = np.array(
        [
            [0, 10, 92, 296, 111, 123, 179, 87],
            [10, 0, 91, 295, 119, 206, 55, 159],
            [92, 91, 0, 205, 129, 93, 217, 76],
            [296, 295, 205, 0, 336, 185, 224, 54],
            [111, 119, 129, 336, 0, 137, 202, 98],
            [123, 206, 93, 185, 137, 0, 208, 71],
            [179, 55, 217, 224, 202, 208, 0, 126],
            [87, 159, 76, 54, 98, 71, 126, 0],
        ]
    )

    best_path, min_distance, gens = tsp_gen(8, 4, cities, adj_matrix, 1000)

    print("Nejlepší cesta:", best_path)
    print("Vzdálenost:", min_distance)

    title = " -> ".join(best_path)

    fig = px.line(
        x=[i[0] for i in gens],
        y=[i[1] for i in gens],
        title=f"Optimální cesta: {title}",
        labels={"x": "Generace", "y": "Fitness value"},
    )
    fig.show()
