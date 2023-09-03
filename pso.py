import random
import numpy as np
import plotly.express as px
import os
from PIL import Image
import imageio


def f(x, y):
    # return (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2
    return (x+2*y-7)**2+(2*x+y-5)**2 # (1,3)


def new_velocity(
    particles, velocity, particle_best, global_best, max=1, w=0.5, c1=0.5, c2=1
):
    new_velocity = np.zeros(len(particles))
    random1 = random.uniform(0, max)
    random2 = random.uniform(0, max)
    for i in range(len(particles)):
        new_velocity[i] = (
            w * velocity[i]
            + c1 * random1 * (particle_best[i] - particles[i])
            + c2 * random2 * (global_best[i] - particles[i])
        )

    return new_velocity


def pso(population, position_min, position_max, epsilon=10e-4):
    particles = [
        [random.uniform(position_min, position_max) for j in range(2)]
        for i in range(population)
    ]
    particle_best_fitness = [f(particle[0], particle[1]) for particle in particles]
    particle_best = [
        [random.uniform(position_min, position_max) for j in range(2)]
        for i in range(population)
    ]
    glob_best = np.argmin(particle_best_fitness)
    glob_best_position = particles[glob_best]
    velocity = np.zeros((population, 2))
    gen = 0

    while np.average(particle_best_fitness) > epsilon:
        gen += 1
        for n in range(population):
            velocity[n] = new_velocity(
                particles[n],
                velocity[n],
                particle_best[n],
                glob_best_position,
            )
            particles[n] = particles[n] + velocity[n]
            if f(particles[n][0], particles[n][1]) < particle_best_fitness[n]:
                particle_best[n] = particles[n]
                particle_best_fitness[n] = f(particles[n][0], particles[n][1])
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

    pso(population, position_min, position_max)

    frames = []
    image_files2 = os.listdir(directory)
    image_files2.sort(key=lambda x: int(x.split(".")[0]))

    for image_file in image_files2:
        image_path = os.path.join(directory, image_file)
        image = Image.open(image_path)

        frames.append(image)

    imageio.mimsave("gifs/pso.gif", frames, duration=frame_duration)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        os.remove(file_path)
