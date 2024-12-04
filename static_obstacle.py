import pygame, sys, time

class StaticObstacle:
    def __init__(self, screen, pos, width, height, color):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.color = color
        self.screen = screen
        self.rect = pygame.draw.rect(self.screen, self.color, (self.x, self.y, width, height))
        self.old_rect = self.rect.copy()

    def generateStaticObstacle(self):
        """Generates a static obstacle in the middle of the screen"""
        static_square = Square((self.windowWidth * 0.5, self.windowHeight * 0.5))
        static_square.width = 300
        static_square.height = 50
        static_square.color = (0, 0, 0)
        self.squares.append(static_square)

    def draw(self):
        self.rect = pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
