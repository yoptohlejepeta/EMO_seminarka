import random
import plotly.express as px


def f(max_weight, items, alpha):
    weight = 0
    value = 0
    for i in range(len(alpha)):
        if alpha[i] == 1 and (weight + items[i][0]) < max_weight:
            weight += items[i][0]
            value += items[i][1]
    
    return value

def mutate(alpha):
    swap = random.sample(range(len(alpha)), 2)
    while alpha[swap[0]] == alpha[swap[1]]:
        swap = random.sample(range(len(alpha)), 2)
    alpha[swap[0]], alpha[swap[1]] = alpha[swap[1]], alpha[swap[0]]
    
    return alpha


def blind_algorithm(tmax, items, max_weight):
    f_fin = 0
    iters = []
    for i in range(tmax):
        alpha = [random.choice([0,1]) for i in range(len(items))]
        iters.append((i, f_fin))
        if f(max_weight, items, alpha) > f_fin:
            alpha_max = alpha
            f_fin = f(max_weight, items, alpha)
    
    return alpha_max, f_fin, iters

def hill_climb(tmax, items, max_weight):
    iters = []
    alpha_max = [random.choice([0,1]) for i in range(len(items))]
    f_fin = f(max_weight, items, alpha_max)
    for time in range(tmax + 1):
        new_alpha = mutate(alpha_max)
        f_x = f(max_weight, items, new_alpha)
        if f_x > f_fin:
            f_fin =  f_x
            alpha_max = new_alpha
        iters.append((time, f_fin))
    
    return alpha_max, f_fin, iters


if __name__ == "__main__":

    items = [(1, 10),
                (1, 100),
                (1, 150),
                (1, 100),
                (1, 100),
                (2, 180), 
                (2, 180), 
                (2, 500), 
                (2, 300), 
                (5, 400), 
                (5, 400), 
                (5, 700), 
                (10, 800), 
                (10, 1000)]

    alpha_max, f_fin, iters = blind_algorithm(100, items, 30)
    best = "".join(map(str, alpha_max))

    fig = px.line(
        x=[i[0] for i in iters],
        y=[i[1] for i in iters],
        labels={"x": "Iterace", "y": "Fitness"},
        title=f"Slepý algoritmus: {best}"
    )
    fig.show()

    alpha_max, f_fin, iters = hill_climb(100, items, 30)
    best = "".join(map(str, alpha_max))

    fig = px.line(
        x=[i[0] for i in iters],
        y=[i[1] for i in iters],
        labels={"x": "Iterace", "y": "Fitness"},
        title=f"Horolezec: {best}"
    )
    fig.show()