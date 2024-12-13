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
        """Checks gravity and apply to object."""
        if not self.obj.selected:
            # Apply gravity
            if self.obj.init_position[1] < windowHeight - self.obj.height - 5:
                self.obj.y_velocity += gravity
            else:
                if abs(self.obj.y_velocity) > bounce_stop:
                    self.obj.y_velocity = -self.obj.y_velocity * self.obj.retention
                else:
                    if abs(self.obj.y_velocity) <= bounce_stop:
                        self.obj.y_velocity = 0

        # Check for collisions with left and right walls
        if self.obj.init_position[0] < self.obj.radius + 5 and self.obj.x_velocity < 0:  # Left wall
            self.obj.init_position[0] = self.obj.radius + 5
            self.obj.x_velocity *= -1 * self.obj.retention
        elif self.obj.init_position[0] > windowWidth - self.obj.radius - 5 and self.obj.x_velocity > 0:  # Right wall
            self.obj.init_position[0] = windowWidth - self.obj.radius - 5
            self.obj.x_velocity *= -1 * self.obj.retention

        if self.obj.y_velocity == 0:
            if abs(self.obj.x_velocity) > 0.20: 
                self.obj.x_velocity *= (1 - self.obj.friction)
            else:
                self.obj.x_velocity = 0

        if self.obj.y_velocity == 0 and self.obj.x_velocity == 0:
            print(f"Ball {self.obj.id} is at rest.")
            print(f"Position: {self.obj.init_position}, Velocity: {self.obj.x_velocity}, {self.obj.y_velocity}")

        return self.obj.y_velocity

    def update_pos(self, mouse_pos):
        """Updates position based on if the object is selected"""
        if not self.obj.selected:
            self.obj.init_position[1] += self.obj.y_velocity
            self.obj.init_position[0] += self.obj.x_velocity
        else:
           self.obj.init_position[0] = mouse_pos[0]
           self.obj.init_position[1] = mouse_pos[1]


class GravityForCircle:
    def __init__(self, obj) -> None:
        self.obj = obj
        self.floating_mode = False
 
    def check_gravity(self, obj):
        """Adjusts the velocity of the object with variables such as gravity, retention and bounce_stop.
        It also handles situation where a circle bounces into any of the walls and adjusts the velocity in turn."""
        if not obj.selected:
                if obj.init_position[1] + obj.radius <= windowHeight - obj.radius - 10:
                    obj.y_velocity += gravity
                else:
                    if abs(obj.y_velocity) > bounce_stop:
                        obj.y_velocity = obj.y_velocity * -1 * obj.retention
                    else:
                        if abs(obj.y_velocity) <= bounce_stop:
                            obj.y_velocity = 0

        # Collision with left and right walls (X-axis)
        if (obj.init_position[0] + obj.radius < obj.radius + 10 and obj.x_velocity < 0) or \
           (obj.init_position[0] + obj.radius > windowWidth - obj.radius - 10 and obj.x_velocity > 0):
            obj.x_velocity *= -1 * obj.retention
            if abs(obj.x_velocity) < bounce_stop:
                obj.x_velocity = 0

        # Collision with top wall (Y-axis)**
        if obj.init_position[1] - obj.radius < 0 - obj.radius:
            obj.y_velocity *= -1 * obj.retention
            obj.init_position[1] = obj.radius
            if abs(obj.y_velocity) < bounce_stop:
                obj.y_velocity = 0

        if obj.y_velocity == 0:
            if abs(obj.x_velocity) > obj.friction:
                if obj.x_velocity > 0:
                    obj.x_velocity -= obj.friction
                elif obj.x_velocity < 0:
                    obj.x_velocity += obj.friction 
            else:
                obj.x_velocity = 0

        if obj.init_position[1] + obj.radius < 0 +  obj.radius:
            obj.init_position[1] = 0 + obj.radius

        return obj.y_velocity
    
    def update_pos(self, obj, mouse_pos):
        """Updates position based on if the object is selected"""
        if not obj.selected:
            obj.init_position[1] += obj.y_velocity
            obj.init_position[0] += obj.x_velocity
        else:
           obj.init_position[0] = mouse_pos[0]
           obj.init_position[1] = mouse_pos[1]

