import random
import math
import pygame
import matplotlib.pyplot as plt
import numpy as np
from Particle import Particle, Plant, SurfaceWater, SoilWater


def brownian_motion() -> float:
    return np.random.normal(0,1)


if __name__ == "__main__":
    pygame.init()

    diffusion_coef = 1.0
    attraction_coef = 100.0

    width, height = 500, 500
    screen = pygame.display.set_mode((width, height), flags=pygame.SCALED)

    # Time parameters
    time_step = 0.1
    clock = pygame.time.Clock()
    pygame_start_time = pygame.time.get_ticks()
    real_time = 0

    is_running = True

    nb_particles = 100
    particles = [Particle(width * random.random(), height * random.random(), 2 * random.random() - 1,
                          2 * random.random() - 1, 3) for _ in range(nb_particles)]

    plants = [Plant(width * random.random(), height * random.random(), 2 * random.random() - 1,
                          2 * random.random() - 1, 3) for _ in range(nb_particles // 3)]
    surface_waters = [SurfaceWater(width * random.random(), height * random.random(), 2 * random.random() - 1,
                          2 * random.random() - 1, 3) for _ in range(nb_particles // 3)]
    soil_waters = [SoilWater(width * random.random(), height * random.random(), 2 * random.random() - 1,
                                   2 * random.random() - 1, 3) for _ in range(nb_particles // 3)]

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

        screen.fill(pygame.color.Color("white"))

        pygame.display.set_caption(f"Arid Ecosystem Simulation\tFPS: {int(clock.get_fps())}")

        for p in plants:
            p.draw(screen)
            p.x += (math.sqrt(time_step / 2) * brownian_motion() -
                    time_step * attraction_coef * p.attraction_along_x(particles) / nb_particles)
            p.y += (math.sqrt(time_step / 2) * brownian_motion() -
                    time_step * attraction_coef * p.attraction_along_y(particles) / nb_particles)

        for o in surface_waters:
            o.draw(screen)
            o.x += math.sqrt(time_step / 2) * brownian_motion()
            o.y += math.sqrt(time_step / 2) * brownian_motion()

        for w in soil_waters:
            w.draw(screen)
            w.x += math.sqrt(time_step / 2) * brownian_motion()
            w.y += math.sqrt(time_step / 2) * brownian_motion()

        pygame.display.flip()
        clock.tick(60)  # limitation des fps à 60

    end_time = pygame.time.get_ticks()
    total_time = end_time - pygame_start_time
    pygame.quit()