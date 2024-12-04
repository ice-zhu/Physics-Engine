import random
import pygame

class Square:
    def __init__(self, init_position, gravity=None):
        #id gives the square a unique identifier to refer to
        #id will be generated by the physics engine in its loop
        #retention = slow down the bounce
        self.width = random.uniform(30.0, 100.0)
        self.height = random.uniform(30.0, 100.0)
        self.color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))  # Random RGB color
        self.init_position = list(init_position) #marks where the square was initially created
        self.y_velocity = 0
        self.x_velocity = 0
        self.retention = 0.9        
        self.mass = 200

        if gravity is None:
            self.gravity = Gravity(self)
        else:
            self.gravity = gravity

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.init_position[0], self.init_position[1], self.width, self.height))

    def setID(self, id):
        self.id = id

    def apply(self):
        self.gravity.check_gravity()
        self.gravity.update_pos()

    def contains_point(self, point):
        """Check if the point (x, y) is inside this square"""
        px, py = point
        return self.init_position[0] <= px <= self.init_position[0] + self.width and self.init_position[1] <= py <= self.init_position[1] + self.height

class Gravity:
    gravity = 0.5
    bounce_stop = 0.5

    def __init__(self, obj) -> None:
        self.windowHeight = 600
        self.obj = obj
    
    def check_gravity(self):
        """make the object extend gravity or that every object has the functionalities of gravity -- REWRITE"""
        if self.obj.init_position[1] < self.windowHeight - self.obj.height - 5:
            self.obj.y_velocity += Gravity.gravity
        else:
            if abs(self.obj.y_velocity) > Gravity.bounce_stop:
                self.obj.y_velocity = -self.obj.y_velocity  * self.obj.retention
            else:
                if abs(self.obj.y_velocity) <= Gravity.bounce_stop:
                    self.obj.y_velocity = 0
        
        return self.obj.y_velocity
    
    def update_pos(self):
        self.obj.init_position[1] += self.obj.y_velocity
        self.obj.init_position[0] += self.obj.x_velocity