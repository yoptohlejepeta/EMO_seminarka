import random
import numpy as np
import plotly.express as px
import os
from PIL import Image
import imageio



def f(x, y):
    return (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2


def new_velocity(particles, velocity, pbest, gbest, w_min=0.5, max=1, c1=1, c2=0.1):
    new_velocity = np.zeros(len(particles))
    random1 = random.uniform(0, max)
    random2 = random.uniform(0, max)
    w = random.uniform(w_min, max)
    for i in range(len(particles)):
        new_velocity[i] = (
            w * velocity[i] + c1 * random1 * (pbest[i] - particles[i]) + c2 * random2 * (gbest[i] - particles[i])
        )

    return new_velocity


def pso(
    population, position_min, position_max
):
    particles = [
        [random.uniform(position_min, position_max) for j in range(2)]
        for i in range(population)
    ]
    particle_best_fitness = [f(particle[0], particle[1]) for particle in particles]
    glob_best = np.argmin(particle_best_fitness)
    glob_best_position = particles[glob_best]
    velocity = [[0 for j in range(2)] for i in range(population)]
    gen = 0

    while np.average(particle_best_fitness) > epsilon:
        gen += 1

        for n in range(population):
            velocity[n] = new_velocity(
                particles[n], velocity[n], particles[n], glob_best_position
            )
            particles[n] = particles[n] + velocity[n]
        particle_best_fitness = [f(p[0], p[1]) for p in particles]
        glob_best = np.argmin(particle_best_fitness)
        glob_best_position = particles[glob_best]

        fig = px.scatter(x=np.array(particles)[:, 0], y=np.array(particles)[:, 1])
        fig.update_layout(yaxis_range=[position_min, position_max])
        fig.update_layout(xaxis_range=[position_min, position_max])
        fig.update_yaxes(scaleratio=1)
        fig.update_xaxes(scaleratio=1)
        fig.write_image(f"images/{gen}.png")

    print("Glob. nejlepsi: ", glob_best_position)
    print("Nejlepsi fitness: ", min(particle_best_fitness))
    print("Pocet generaci: ", gen)

    return particles


if __name__ == "__main__":

    directory = "images/"
    frame_duration = 100
    image_files1 = os.listdir(directory)
    
    population = 50
    position_min = -10
    position_max = 10
    epsilon = 10e-4


    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        os.remove(file_path)


    pso(
        population, position_min, position_max
    )

    frames = []
    image_files2 = os.listdir(directory)
    image_files2.sort(key=lambda x: int(x.split(".")[0]))


    for image_file in image_files2:
        image_path = os.path.join(directory, image_file)
        image = Image.open(image_path)

        frames.append(image)
    imageio.mimsave("gifs/pso.gif", frames, duration=frame_duration)