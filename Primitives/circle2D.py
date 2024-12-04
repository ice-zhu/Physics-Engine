import random
import pygame
from Primitives.gravity import GravityForCircle as Gravity

class Circle:
    def __init__(self, init_position, gravity=None):
        #retention = slow down the bounce
        self.radius = random.uniform(30.0, 50.0)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))  # Random RGB color
        self.init_position = list(init_position) #marks where the circle was initially created
        self.y_velocity = 0
        self.x_velocity = 0
        self.retention = 0.9        
        self.mass = 200
        self.selected = False
        self.friction = 0.1
        self.out_of_bounds = False

        if gravity is None: #Singleton
            self.gravity = Gravity(self)
        else:
            self.gravity = gravity
        
        self.circle = pygame.Rect(self.init_position[0] - self.radius, self.init_position[1] - self.radius, 2 * self.radius, 2 * self.radius)

        self.old_circle = self.circle.copy()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.circle.center, self.radius)

    def setID(self, id):
        self.id = id

    def setOutOfBounds(self, out_of_bounds, screen):
        self.out_of_bounds = out_of_bounds
        if self.out_of_bounds:
            print('Square', {self.id}, 'is out of bounds')
        self.draw(screen)
        print('Square is out of bounds')

    def setSelected(self, selected):
        self.selected = selected
        if self.selected:
            print(self.id, ' has been selected')

    def apply(self, mouse_pos):
        self.gravity.check_gravity(self)
        self.gravity.update_pos(self, mouse_pos)
        self.circle.x = self.init_position[0]
        self.circle.y = self.init_position[1]

    def contains_point(self, point):
        """Check if the mouse's position is inside this square"""
        px, py = point
        if self.circle.collidepoint(px, py):
            print('Square', self.id, 'has been clicked')
        return self.circle.collidepoint(px, py)
    
    def reset_pos(self, windowWidth, windowHeight):
        self.init_position[0] = windowWidth / 2
        self.init_position[1] = windowHeight / 2

