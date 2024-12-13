import math
from Primitives.shape_type import ShapeType
EPSILON = 1e-6
windowWidth = 800
windowHeight = 600

class CollisionManager:
    
    @staticmethod
    def handle_collision(obj1, obj2):
        '''Checks what kind of objects it has received in its parameters and then applies the relevant logic to the objects.'''
        if obj1 is not None and obj2 is not None:
            if obj1.type == ShapeType.CIRCLE and obj2.type == ShapeType.CIRCLE:
                if CollisionForCircle.check_collision(obj1, obj2):
                    CollisionForCircle.resolve_collision(obj1, obj2)
            elif obj2.type == ShapeType.CIRCLE and obj1.type == ShapeType.CIRCLE:
                if CollisionForCircle.check_collision(obj2, obj1):
                    CollisionForCircle.resolve_collision(obj2, obj1)
            elif obj1.type == ShapeType.CIRCLE and obj2.type == ShapeType.SQUARE:
                if MixedCollision.check_circle_square_collision(obj1, obj2):
                    MixedCollision.resolve_circle_square_collision(obj1, obj2)
            elif obj1.type == ShapeType.SQUARE and obj2.type == ShapeType.CIRCLE:
                if MixedCollision.check_circle_square_collision(obj2, obj1):
                    MixedCollision.resolve_circle_square_collision(obj2, obj1)


class CollisionForSquare:
    """To deal with collision among other squares primarily."""

    @staticmethod
    def check_collision(square1, square2):
        """Checks if two squares are colliding."""
        if square1.rect.colliderect(square2.rect):
            square1.color = (255, 0, 0)  # Change color when colliding
        return square1.rect.colliderect(square2.rect)

    @staticmethod
    def resolve_collision(square1, square2):
        """Resolves the collision between two squares."""
        overlap_x = min(square1.rect.right, square2.rect.right) - max(square1.rect.left, square2.rect.left)
        overlap_y = min(square1.rect.bottom, square2.rect.bottom) - max(square1.rect.top, square2.rect.top)

        if overlap_x > 0 and overlap_y > 0:
            if overlap_x < overlap_y:
                if square1.rect.centerx < square2.rect.centerx:
                    square1.rect.right -= overlap_x
                    square2.rect.left = square1.rect.right
                    square1.x_velocity *= -1 * square1.retention
                    if abs(square1.x_velocity) < square1.gravity.bounce_stop:
                        square1.x_velocity = 0 
                else:
                    square1.rect.left += overlap_x
                    square2.rect.right = square1.rect.left
                    square1.x_velocity *= -1 * square1.retention
                    if abs(square1.x_velocity) < square1.gravity.bounce_stop:
                        square1.x_velocity = 0
            else:
                if square1.rect.centery < square2.rect.centery:
                    square1.rect.bottom -= overlap_y
                    square2.rect.top = square1.rect.bottom
                    square1.y_velocity *= -1 * square1.retention
                    if abs(square1.y_velocity) < square1.gravity.bounce_stop:
                        square1.y_velocity = 0
                else:
                    square1.rect.top += overlap_y
                    square2.rect.bottom = square1.rect.top
                    square1.y_velocity *= -1 * square1.retention
                    if abs(square1.y_velocity) < square1.gravity.bounce_stop:
                        square1.y_velocity = 0

            if abs(square1.x_velocity) < square1.gravity.bounce_stop:
                square1.x_velocity = 0 
                square1.init_position[0] = square1.rect.x 

            if abs(square1.y_velocity) < square1.gravity.bounce_stop:
                square1.y_velocity = 0
                square1.init_position[1] = square1.rect.y-square2.rect.y

class CollisionForCircle:
    @staticmethod
    def check_collision(circle1, circle2):
        '''Checks if two circles are colliding by measuring the distance between them. If true, it will change the color of the circles.'''
        dx1 = circle1.init_position[0] - circle2.init_position[0]
        dy1 = circle1.init_position[1] - circle2.init_position[1]
        distance1 = math.sqrt(dx1 ** 2 + dy1 ** 2)

        if distance1 < (circle1.radius + circle2.radius): 
            if circle1.color != (255, 0, 0):
                circle1.color = (255, 0, 0)
            if circle2.color != (255, 0, 0):
                circle2.color = (255, 0, 0)
            return True  
        else:
            if circle1.color == (255, 0, 0): 
                circle1.color = circle1.original_color
            if circle2.color == (255, 0, 0): 
                circle2.color = circle2.original_color
            return False

    @staticmethod
    def resolve_collision(circle1, circle2):
        """Resolves the collision between two circles."""
        dx = circle1.init_position[0] - circle2.init_position[0]
        dy = circle1.init_position[1] - circle2.init_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Check if circles are colliding
        if distance <= (circle1.radius + circle2.radius):
            overlap = (circle1.radius + circle2.radius) - distance

            nx = dx / distance if distance > EPSILON else 0
            ny = dy / distance if distance > EPSILON else 0

            circle1.init_position[0] += nx * (overlap * 0.5)
            circle1.init_position[1] += ny * (overlap * 0.5)
            circle2.init_position[0] -= nx * (overlap * 0.5)
            circle2.init_position[1] -= ny * (overlap * 0.5)

            if circle1.init_position[1] + circle1.radius > windowHeight + 10:
                circle1.init_position[1] = windowHeight - circle1.radius
                circle1.y_velocity = 0 

            if circle2.init_position[1] + circle2.radius > windowHeight + 10:
                circle2.init_position[1] = windowHeight - circle2.radius
                circle2.y_velocity = 0 

            if (circle2.init_position[0] + circle2.radius < circle2.radius + 10 and circle2.x_velocity < 0) or \
            (circle2.init_position[0] + circle2.radius > windowWidth - circle2.radius - 10 and circle2.x_velocity > 0):
                circle2.init_position[0] *= -1 * circle2.retention

            if (circle1.init_position[0] + circle1.radius < circle1.radius + 10 and circle1.x_velocity < 0) or \
            (circle1.init_position[0] + circle1.radius > windowWidth - circle1.radius - 10 and circle1.x_velocity > 0):
                circle1.init_position[0] *= -1 * circle1.retention

            relative_velocity_x = circle1.x_velocity - circle2.x_velocity
            relative_velocity_y = circle1.y_velocity - circle2.y_velocity

            dot_product = relative_velocity_x * nx + relative_velocity_y * ny

            # If the circles are moving towards each other, resolve the collision
            if dot_product < 0:
                impulse = 2 * dot_product / (circle1.mass + circle2.mass)

                circle1.x_velocity -= impulse * circle2.mass * nx
                circle1.y_velocity -= impulse * circle2.mass * ny
                circle2.x_velocity += impulse * circle1.mass * nx
                circle2.y_velocity += impulse * circle1.mass * ny

                circle1.x_velocity *= circle1.retention
                circle1.y_velocity *= circle1.retention
                circle2.x_velocity *= circle2.retention
                circle2.y_velocity *= circle2.retention

                if abs(circle1.x_velocity) <= circle1.friction:
                    circle1.x_velocity = 0
                if abs(circle1.y_velocity) <= circle1.friction:
                    circle1.y_velocity = 0
                if abs(circle2.x_velocity) <= circle2.friction:
                    circle2.x_velocity = 0
                if abs(circle2.y_velocity) <= circle2.friction:
                    circle2.y_velocity = 0

        return circle1, circle2

class MixedCollision: 
    @staticmethod
    def check_circle_square_collision(circle, square):
        """Check collision between a circle and a square."""
        cx = circle.init_position[0]
        cy = circle.init_position[1]
        radius = circle.radius

        left = square.rect.left - circle.radius
        right = square.rect.right - circle.radius
        top = square.rect.top -circle.radius
        bottom = square.rect.bottom - circle.radius

        nearest_x = max(left, min(cx, right))
        nearest_y = max(top, min(cy, bottom)) 

        dx = cx - nearest_x
        dy = cy - nearest_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= radius:
            MixedCollision.change_color_of_object(circle, square, True)
        else:
            MixedCollision.change_color_of_object(circle, square, False)

        return distance <= radius


    @staticmethod
    def change_color_of_object(circle, square, is_colliding):
        """Change the color of the object when they collide."""
        if is_colliding:
            if circle.color != (255, 0, 0):
                circle.color = (255, 0, 0)
            if square.color != (255, 0, 0):
                square.color = (255, 0, 0)
        else:
            if circle.color == (255, 0, 0): 
                circle.color = circle.original_color
            if square.color == (255, 0, 0): 
                square.color = square.original_color
    

    @staticmethod
    def resolve_circle_square_collision(circle, square):
        radius = circle.radius
        nearest_x = max(square.rect.left - radius, min(circle.init_position[0], square.rect.right-radius))
        nearest_y = max(square.rect.top - radius, min(circle.init_position[1], square.rect.bottom - radius))

        dx = circle.init_position[0] - nearest_x
        dy = circle.init_position[1] - nearest_y
        distance = math.sqrt(dx**2 + dy**2)
        overlap = circle.radius - distance

        if overlap > 0:
            nx = dx / distance if distance > EPSILON else 0
            ny = dy / distance if distance > EPSILON else 0

            circle.init_position[0] += nx * overlap
            circle.init_position[1] += ny * overlap

            dot_product = circle.x_velocity * nx + circle.y_velocity * ny
            circle.x_velocity -= 2 * dot_product * nx
            circle.y_velocity -= 2 * dot_product * ny

            circle.x_velocity *= circle.retention
            circle.y_velocity *= circle.retention

        if abs(circle.init_position[1] + circle.radius - square.rect.top) < EPSILON and circle.y_velocity > 0:
            circle.y_velocity = 0
            circle.init_position[1] = square.rect.top - circle.radius