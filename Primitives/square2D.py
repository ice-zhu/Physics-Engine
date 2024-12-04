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

class Gravity:
    gravity = 0.5
    bounce_stop = 0.5

    def __init__(self, obj) -> None:
        self.windowHeight = 600
        self.windowWidth = 800
        self.obj = obj
        self.bounce_stop = 0.5
    
    def check_gravity(self):
        """Check gravity and apply to object"""
        if not self.obj.selected:
            if self.obj.init_position[1] < self.windowHeight - self.obj.height - 5:
                self.obj.y_velocity += Gravity.gravity
            else:
                if abs(self.obj.y_velocity) > Gravity.bounce_stop:
                    self.obj.y_velocity = -self.obj.y_velocity * self.obj.retention
                else:
                    if abs(self.obj.y_velocity) <= Gravity.bounce_stop:
                        self.obj.y_velocity = 0
        if (self.obj.init_position[0] < self.obj.height + (5/2) and self.obj.x_velocity < 0) or (self.obj.init_position[0] > self.windowWidth - self.obj.width - (5/2) and self.obj.x_velocity > 0):
            self.obj.x_velocity *= -1 * self.retention
            if abs(self.obj.x_velocity) < self.bounce_stop:
                self.obj.x_velocity = 0
        if self.obj.y_velocity == 0 and self.obj.x_velocity > 0:
            self.obj.x_velocity -= self.obj.friction
        elif self.obj.y_velocity == 0 and self.obj.x_velocity < 0:
            self.obj.x_velocity += self.obj.friction

        return self.obj.y_velocity
    
    def update_pos(self, mouse_pos):
        self.obj.old_rect = self.obj.rect.copy() #previous frame

        """Update position based on velocity"""
        if not self.obj.selected:
            self.obj.init_position[1] += self.obj.y_velocity
            self.obj.init_position[0] += self.obj.x_velocity
        else:
           self.obj.init_position[0] = mouse_pos[0]
           self.obj.init_position[1] = mouse_pos[1]


        