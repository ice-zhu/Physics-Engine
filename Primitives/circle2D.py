import random
import pygame
from Primitives.gravity import GravityForCircle as Gravity
from Primitives.shape_type import ShapeType
from Primitives.shape2D import Shape

class Circle(Shape):
    def __init__(self, init_position, gravity=None):
        self.type = ShapeType.CIRCLE
        self.radius = 50
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
        self.init_position = list(init_position)
        self.y_velocity = 0
        self.x_velocity = 0
        self.retention = random.uniform(0.5, 0.9)        
        self.mass = random.uniform(100, 300)
        self.selected = False
        self.friction = 0.3
        self.out_of_bounds = False
        self.original_color = self.color

        if gravity is None: #Singleton
            self.gravity = Gravity(self)
        else:
            self.gravity = gravity
        self.circle = pygame.Rect(self.init_position[0] - self.radius, self.init_position[1] - self.radius, 2 * self.radius, 2 * self.radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.circle.center, self.radius)

    def setID(self, id):
        self.id = id

    def setOutOfBounds(self, out_of_bounds, screen):
        self.out_of_bounds = out_of_bounds
        if self.out_of_bounds:
            print('Circle', {self.id}, 'is out of bounds')
        self.draw(screen)

    def setSelected(self, selected):
        self.selected = selected

    def apply(self, mouse_pos):
        '''Apply gravity to the object and update its position.'''
        self.gravity.check_gravity(self)
        self.gravity.update_pos(self, mouse_pos)
        self.circle.x = self.init_position[0]
        self.circle.y = self.init_position[1]

    def contains_point(self, point):
        """Check if the mouse's position is inside this square"""
        px, py = point
        if self.circle.collidepoint(px, py):
            print('Circle', self.id, 'has been clicked')
        return self.circle.collidepoint(px, py)
    
    def reset_pos(self, windowWidth, windowHeight):
        self.init_position[0] = windowWidth / 2
        self.init_position[1] = windowHeight / 2

