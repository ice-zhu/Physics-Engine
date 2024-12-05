import pygame
from Primitives.square2D import Square

#errors with the hitbox, it doesnt align with the circles intersection although both the square and the obstacle itself produces the correct dimensions.
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
        self.static_square = None

    @staticmethod
    def generateStaticObstacle(windowWidth, windowHeight):
        """Generates a static obstacle in the middle of the screen"""
        position = (windowWidth * 0.5, windowHeight * 0.5)
        print('Static obstacle generated at:', position)
        static_square = Square(position, enable_gravity=False)
        static_square.setID(1000)
        return static_square

    def draw(self):
        self.rect = pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def contains_point(self, point):
        """Check if the point is inside the obstacle."""
        return self.rect.collidepoint(point)