import random
import pygame

class Square:
    def __init__(self, x_pos, y_pos, init_position):
        self.width = random.uniform(30.0, 100.0)
        self.height = random.uniform(30.0, 100.0)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))  # Random RGB color
        self.init_position = init_position #marks where the square was initially created

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.width, self.height))

