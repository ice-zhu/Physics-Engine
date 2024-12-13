import random
import pygame
from Primitives.gravity import GravityForSquare as Gravity
from Primitives.shape_type import ShapeType
from Primitives.shape2D import Shape

windowHeight = 600
windowWidth = 800

class Square(Shape):
    def __init__(self, init_position, enable_gravity, is_walls, gravity=None, ):
        self.type = self.shape = ShapeType.SQUARE
        self.enable_gravity = enable_gravity
        
        self.init_position = list(init_position)  # Marks where the square was initially created
        
        if self.enable_gravity:
            self.create_random_square(gravity)
        else:
            if is_walls:
                self.create_wall(gravity)
            else:
                self.create_obstacle(gravity)

        self.y_velocity = 0
        self.x_velocity = 0
        self.selected = False
        self.friction = 0.1
        self.out_of_bounds = False
        print('Square created at:', self.init_position)

    def create_random_square(self, gravity):
        """Creates a random square if gravity is enabled."""
        self.width = random.uniform(30.0, 100.0)
        self.height = random.uniform(30.0, 100.0)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))  # Random RGB color
        self.original_color = self.color
        if gravity is None:  # Singleton
            self.gravity = Gravity(self)
            self.retention = 0.9
            self.mass = 200
        
        self.rect = pygame.Rect(self.init_position[0], self.init_position[1], self.width, self.height)

    def create_obstacle(self, gravity):
        """Creates a static obstacle if gravity is disabled."""
        self.width = 200
        self.height = 5
        self.color = (255, 255, 255)
        self.id = -1
        self.original_color = self.color

        if gravity is not None:
            self.gravity = gravity
        self.rect = pygame.Rect(self.init_position[0], self.init_position[1], self.width, self.height)
        print('Obstacle created at:', self.init_position)

    def create_wall(self, gravity):
        """Creates a static obstacle if gravity is disabled."""
        self.width = windowWidth
        self.height = windowHeight
        self.color = (255, 255, 255)
        self.original_color = self.color

        if gravity is not None:
            self.gravity = gravity
        self.rect = pygame.Rect(self.init_position[0], self.init_position[1], self.width, self.height)
        return self.rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def setID(self, id):
        self.id = id

    def setOutOfBounds(self, out_of_bounds, screen):
        self.out_of_bounds = out_of_bounds
        if self.out_of_bounds:
            print('Square', {self.id}, 'is out of bounds')
        self.draw(screen)

    def setSelected(self, selected):
        self.selected = selected
        if self.selected:
            print(self.id, ' has been selected')

    def apply(self, mouse_pos):
        '''Apply gravity to the object and update its position.'''
        if self.enable_gravity:
            self.gravity.check_gravity()
            self.gravity.update_pos(mouse_pos)
            self.rect.x = self.init_position[0]
            self.rect.y = self.init_position[1]

    def contains_point(self, point):
        """Check if the mouse's position is inside this square"""
        px, py = point
        if self.rect.collidepoint(px, py):
            print('Square', self.id, 'has been clicked')
        return self.rect.collidepoint(px, py)
    
    def reset_pos(self, windowWidth, windowHeight):
        self.init_position[0] = windowWidth / 2
        self.init_position[1] = windowHeight / 2
        