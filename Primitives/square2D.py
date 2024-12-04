import random
import pygame

class Square:
    def __init__(self, init_position, gravity=None):
        #retention = slow down the bounce
        self.width = random.uniform(30.0, 100.0)
        self.height = random.uniform(30.0, 100.0)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))  # Random RGB color
        self.init_position = list(init_position) #marks where the square was initially created
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
        
        self.rect = pygame.Rect(self.init_position[0], self.init_position[1], self.width, self.height)
        self.old_rect = self.rect.copy()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

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
        