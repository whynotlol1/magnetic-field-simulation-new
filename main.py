import time
import math
import pygame
import scipy.integrate as integrate
from particles import Particle


pygame.init()
standart = height = width = 800
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption("magnetic field simulation")
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

magnet_standart = 25
magnet_data = {
    "coords": [375, 375],
    "moving_speed": 0.4,
    "strength": 0.44,  # strength parameter must be greater or equal to 0.35
    "magnetic_lines_direction": "up-down"
}

particle_generated = Particle([0, 0], 0, 0.0, "", (1.6 * 10 ** -19), (1.6 * 10 * -27), False)

if __name__ == '__main__':
    running = True
    while running:

        # drawing the magnet and the magnetic field
        screen.fill((255, 255, 255))
        text_surface = my_font.render(f'magnet strength (induction): {round(magnet_data["strength"], 2)}', False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))
        if magnet_data["magnetic_lines_direction"] == "up-down":
            text_surface = my_font.render(f'magnet pole the viewer sees: N', False, (0, 0, 0))
        else:
            text_surface = my_font.render(f'magnet pole the viewer sees: S', False, (0, 0, 0))
        screen.blit(text_surface, (0, 50))
        pygame.draw.rect(screen, (0, 0, 0), (magnet_data["coords"][0] - magnet_standart / 2, magnet_data["coords"][1] - magnet_standart / 2, magnet_standart, magnet_standart))
        param = integrate.quad(lambda x: magnet_data["strength"] * standart, 0, magnet_data["strength"])[0]
        for i in range(0, width, 5):
            for j in range(0, height, 5):
                if math.sqrt((i - magnet_data["coords"][0]) ** 2 + (j - magnet_data["coords"][1]) ** 2) < param:
                    if magnet_data["magnetic_lines_direction"] == "up-down":
                        pygame.draw.circle(screen, (0, 0, 255), (i, j), 1)
                    else:
                        pygame.draw.circle(screen, (255, 0, 0), (i, j), 1)

        # drawing the particle
        if particle_generated.particle_data["is_seen_on_screen"]:
            if particle_generated.particle_data["charge_sign"] == "+":
                pygame.draw.circle(screen, (255, 0, 0), (particle_generated.particle_data["coords"][0], particle_generated.particle_data["coords"][1]), 5)
            else:
                pygame.draw.circle(screen, (0, 0, 255), (particle_generated.particle_data["coords"][0], particle_generated.particle_data["coords"][1]), 5)

        # removing the particle if it's off-screen
        if particle_generated.particle_data["coords"][0] > width or particle_generated.particle_data["coords"][0] < 0 or particle_generated.particle_data["coords"][1] > height or particle_generated.particle_data["coords"][1] < 0:
            particle_generated.particle_data["is_seen_on_screen"] = False

        # particle movement. the particle moves along the vector which is particle_data["speed_direction"] degrees from the positive x-axis
        if particle_generated.particle_data["is_seen_on_screen"]:
            particle_generated.particle_data["coords"][0] += particle_generated.particle_data["speed"] * math.cos(math.radians(particle_generated.particle_data["speed_direction"]))
            particle_generated.particle_data["coords"][1] += particle_generated.particle_data["speed"] * math.sin(math.radians(particle_generated.particle_data["speed_direction"]))

        # changing the particle's speed direction if it's in the magnetic field
        if math.sqrt((particle_generated.particle_data["coords"][0] - magnet_data["coords"][0]) ** 2 + (particle_generated.particle_data["coords"][1] - magnet_data["coords"][1]) ** 2) < param:
            if magnet_data["magnetic_lines_direction"] == "up-down":
                if particle_generated.particle_data["charge_sign"] == "+":
                    particle_generated.particle_data["speed_direction"] -= (particle_generated.particle_data["charge_value"] * magnet_data["strength"]) / particle_generated.particle_data["mass"] * 10 ** 21
                else:
                    particle_generated.particle_data["speed_direction"] += (particle_generated.particle_data["charge_value"] * magnet_data["strength"]) / particle_generated.particle_data["mass"] * 10 ** 21
            else:
                if particle_generated.particle_data["charge_sign"] == "+":
                    particle_generated.particle_data["speed_direction"] += (particle_generated.particle_data["charge_value"] * magnet_data["strength"]) / particle_generated.particle_data["mass"] * 10 ** 21
                else:
                    particle_generated.particle_data["speed_direction"] -= (particle_generated.particle_data["charge_value"] * magnet_data["strength"]) / particle_generated.particle_data["mass"] * 10 ** 21
        # controls
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and magnet_data["coords"][1] > 0 + magnet_standart / 2:
            magnet_data["coords"][1] -= magnet_data["moving_speed"]
        if keys[pygame.K_s] and magnet_data["coords"][1] < height - magnet_standart / 2:
            magnet_data["coords"][1] += magnet_data["moving_speed"]
        if keys[pygame.K_d] and magnet_data["coords"][0] < width - magnet_standart / 2:
            magnet_data["coords"][0] += magnet_data["moving_speed"]
        if keys[pygame.K_a] and magnet_data["coords"][0] > 0 + magnet_standart / 2:
            magnet_data["coords"][0] -= magnet_data["moving_speed"]

        if keys[pygame.K_1]:
            magnet_data["strength"] += 0.01
            time.sleep(0.2)
        if keys[pygame.K_2]:
            magnet_data["strength"] = magnet_data["strength"] - 0.01 if magnet_data["strength"] > 0.35 else magnet_data["strength"]
            time.sleep(0.2)

        if keys[pygame.K_q]:
            magnet_data["magnetic_lines_direction"] = "up-down" if magnet_data["magnetic_lines_direction"] == "down-up" else "down-up"
            time.sleep(0.2)

        if keys[pygame.K_EQUALS]:
            if not particle_generated.particle_data["is_seen_on_screen"]:
                particle_generated.particle_data["coords"] = [0, 0]
                particle_generated.particle_data["charge_sign"] = "+"
                particle_generated.particle_data["is_seen_on_screen"] = True
                particle_generated.particle_data["speed_direction"] = 45
                particle_generated.particle_data["speed"] = 0.5

        if keys[pygame.K_MINUS]:
            if not particle_generated.particle_data["is_seen_on_screen"]:
                particle_generated.particle_data["coords"] = [0, 0]
                particle_generated.particle_data["charge_sign"] = "-"
                particle_generated.particle_data["is_seen_on_screen"] = True
                particle_generated.particle_data["speed_direction"] = 45
                particle_generated.particle_data["speed"] = 0.5

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit(0)
