import random
import plotly.express as px


def fitness(max_weight, items, alpha):
    value = 0
    weight = 0
    for i in range(len(alpha)):
        if alpha[i] == 1 and (weight + items[i][0]) < max_weight:
            value += items[i][1]
            weight += items[i][0]
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
        if fitness(max_weight, items, alpha) > f_fin:
            alpha_fin = alpha
            f_fin = fitness(max_weight, items, alpha)
    return alpha_fin, f_fin, iters

if __name__ == "__main__":

    predmety = [(1, 100),
                (1, 100),
                (1, 100),
                (1, 100),
                (1, 100),
                (2, 180), 
                (2, 180), 
                (2, 180), 
                (2, 180), 
                (5, 400), 
                (5, 400), 
                (5, 400), 
                (10, 800), 
                (10, 800)]

    alpha_fin, f_fin, iters = blind_algorithm(50, predmety, 30)
    best = "".join(map(str, alpha_fin))

    fig = px.line(
        x=[i[0] for i in iters],
        y=[i[1] for i in iters],
        labels={"x": "Iterace", "y": "Fitness"},
        title=f"Blind algorithm: {best}"
    )
    fig.show()