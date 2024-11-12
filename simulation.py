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

    width = 2100
    height = width // 3
    screen = pygame.display.set_mode((width, height), flags=pygame.SCALED)
    screen_plants = pygame.surface.Surface((width // 3 - 33, height))
    screen_surface_water = pygame.surface.Surface((width // 3 - 33, height))
    screen_soil_water = pygame.surface.Surface((width // 3 - 33, height))


    # Time parameters
    time_step = 0.1
    clock = pygame.time.Clock()
    pygame_start_time = pygame.time.get_ticks()
    real_time = 0

    is_running = True

    nb_particles = 300
    particles = [Particle(width * random.random(), height * random.random(), 2 * random.random() - 1,
                          2 * random.random() - 1, 3) for _ in range(nb_particles)]

    plants = [Plant((width // 3 - 33) * random.random(), height * random.random(), 2 * random.random() - 1,
                          2 * random.random() - 1, 3) for _ in range(nb_particles // 3)]
    surface_waters = [SurfaceWater((width // 3 - 33) * random.random(), height * random.random(), 2 * random.random() - 1,
                          2 * random.random() - 1, 3) for _ in range(nb_particles // 3)]
    soil_waters = [SoilWater((width // 3 - 33) * random.random(), height * random.random(), 2 * random.random() - 1,
                                   2 * random.random() - 1, 3) for _ in range(nb_particles // 3)]

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

        screen_plants.fill(pygame.color.Color("white"))
        screen_surface_water.fill(pygame.color.Color("white"))
        screen_soil_water.fill(pygame.color.Color("white"))

        pygame.display.set_caption(f"Arid Ecosystem Simulation\tFPS: {int(clock.get_fps())}")

        for p in plants:
            p.draw(screen_plants)
            p.x += (math.sqrt(time_step / 2) * brownian_motion() -
                    time_step * attraction_coef * p.attraction_along_x(particles) / nb_particles)
            p.y += (math.sqrt(time_step / 2) * brownian_motion() -
                    time_step * attraction_coef * p.attraction_along_y(particles) / nb_particles)

        for o in surface_waters:
            o.draw(screen_surface_water)
            o.x += math.sqrt(time_step / 2) * brownian_motion()
            o.y += math.sqrt(time_step / 2) * brownian_motion()

        for w in soil_waters:
            w.draw(screen_soil_water)
            w.x += math.sqrt(time_step / 2) * brownian_motion()
            w.y += math.sqrt(time_step / 2) * brownian_motion()

        screen.blit(screen_plants, (0, 0))
        screen.blit(screen_surface_water, (width // 3 - 33 + 50, 0))
        screen.blit(screen_soil_water, (2 * (width // 3 - 33 + 50), 0))
        pygame.display.flip()
        clock.tick(60)  # limitation des fps à 60

    end_time = pygame.time.get_ticks()
    total_time = end_time - pygame_start_time
    pygame.quit()