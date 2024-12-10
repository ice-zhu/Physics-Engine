import random as r
windowHeight = 600
windowWidth = 800
gravity = 0.5
bounce_stop = 0.5

class GravityForSquare:
    def __init__(self, obj) -> None:
        self.obj = obj
        self.bounce_stop = 0.5

    def check_gravity(self):
        """Check gravity and apply to object."""
        if not self.obj.selected:
            if self.obj.init_position[1] < windowHeight - self.obj.height - 5:
                self.obj.y_velocity += gravity
            else:
                if abs(self.obj.y_velocity) > bounce_stop:
                    self.obj.y_velocity = -self.obj.y_velocity * self.obj.retention
                else:
                    if abs(self.obj.y_velocity) <= bounce_stop:
                            self.obj.y_velocity = 0
        
        if (self.obj.init_position[0] + self.obj.radius < self.obj.height and self.obj.x_velocity < 0) or (self.obj.init_position[0] + self.obj.radius > windowWidth and self.obj.x_velocity > 0):
            self.obj.x_velocity *= -1 * self.retention
            if abs(self.obj.x_velocity) < self.bounce_stop:
                self.obj.x_velocity = 0
 
        if self.obj.y_velocity == 0 and self.obj.x_velocity > 0:
            self.obj.x_velocity -= self.obj.friction
        elif self.obj.y_velocity == 0 and self.obj.x_velocity < 0:
            self.obj.x_velocity += self.obj.friction
        elif self.obj.y_velocity == 0 and self.obj.x_velocity == 0:
            self.obj.x_velocity = 0

        return self.obj.y_velocity
    
    def update_pos(self, mouse_pos):
        """Update position based on velocity"""
        self.obj.old_rect = self.obj.rect.copy()  # previous frame

        if not self.obj.selected:
            self.obj.init_position[1] += self.obj.y_velocity
            self.obj.init_position[0] += self.obj.x_velocity
        else:
           self.obj.init_position[0] = mouse_pos[0]
           self.obj.init_position[1] = mouse_pos[1]

class GravityForCircle:
    def __init__(self, obj) -> None:
        self.obj = obj
        self.floating_mode = False # objects will fall automatically upon initialization
 
    def check_gravity(self, obj):
        """Check gravity and apply to object."""
        if not obj.selected:
                if obj.init_position[1] + obj.radius <= windowHeight - obj.radius - 10:
                    obj.y_velocity += gravity
                else:
                    if abs(obj.y_velocity) > bounce_stop:
                        obj.y_velocity = obj.y_velocity * -1 * obj.retention
                    else:
                        if abs(obj.y_velocity) <= bounce_stop:
                            obj.y_velocity = 0

        #Collision with left and right walls (X-axis)
        if (obj.init_position[0] < obj.radius + 10 and obj.x_velocity < 0) or \
           (obj.init_position[0] > windowWidth - obj.radius - 10 and obj.x_velocity > 0):
            obj.x_velocity *= -1 * obj.retention
            if abs(obj.x_velocity) < bounce_stop:
                obj.x_velocity = 0

        #Collision with top wall (Y-axis)**
        if obj.init_position[1] - obj.radius < 0 - obj.radius:
            obj.y_velocity *= -1 * obj.retention
            obj.init_position[1] = obj.radius #correct this
            print(obj.init_position[1], " is here !!!!") #remove when fixed
            if abs(obj.y_velocity) < bounce_stop:
                obj.y_velocity = 0

        if obj.y_velocity == 0 and obj.x_velocity > 0:
            obj.x_velocity -= obj.friction
        elif obj.y_velocity == 0 and obj.x_velocity < 0:
            obj.x_velocity += obj.friction

        return obj.y_velocity
    
    def update_pos(self, obj, mouse_pos):
        """Update position based on velocity."""
        if not obj.selected:
            obj.init_position[1] += obj.y_velocity
            obj.init_position[0] += obj.x_velocity
        else:
           obj.init_position[0] = mouse_pos[0]
           obj.init_position[1] = mouse_pos[1]

