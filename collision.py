import math
EPSILON = 1e-6


from Primitives.shape_type import ShapeType

class CollisionManager:
    @staticmethod
    def handle_collision(obj1, obj2):
        if obj1 is not None and obj2 is not None:
            if obj1.type == ShapeType.CIRCLE and obj2.type == ShapeType.CIRCLE:
                if CollisionForCircle.check_collision(obj1, obj2):
                    CollisionForCircle.resolve_collision(obj1, obj2)
            elif obj1.type == ShapeType.SQUARE and obj2.type == ShapeType.SQUARE:
                if CollisionForSquare.check_collision(obj1, obj2):
                    CollisionForSquare.resolve_collision(obj1, obj2)
            elif obj1.type == ShapeType.CIRCLE and obj2.type == ShapeType.SQUARE:
        
                if MixedCollision.check_circle_square_collision(obj1, obj2):
                    
                    MixedCollision.resolve_circle_square_collision(obj1, obj2)
            elif obj1.type == ShapeType.SQUARE and obj2.type == ShapeType.CIRCLE:
                if MixedCollision.check_circle_square_collision(obj2, obj1):
                    print("Collision between square + circle")
                    MixedCollision.resolve_circle_square_collision(obj2, obj1)


class CollisionForSquare:
    """To deal with collision among other squares primarily."""

    @staticmethod
    def check_collision(square1, square2):
        """Check if two squares are colliding."""
        if square1.rect.colliderect(square2.rect):
            square1.color = (255, 0, 0)  # Change color when colliding, see if to update in realtime
        return square1.rect.colliderect(square2.rect)

    @staticmethod
    def resolve_collision(square1, square2):
        """Resolve the collision between two squares."""
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
    """To deal with collision among circle objects."""

    @staticmethod
    def check_collision(circle1, circle2):
        """Check if two circles are colliding."""
        dx = circle1.init_position[0] - circle2.init_position[0]
        dy = circle1.init_position[1] - circle2.init_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2 + 5)

        if distance <= (circle1.radius + circle2.radius): #polish this algorithm assumes that circle 1 is bigger when some circles are smaller
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
        """Resolve the collision between two circles."""
        dx = circle1.init_position[0] - circle2.init_position[0]
        dy = circle1.init_position[1] - circle2.init_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < (circle1.radius + circle2.radius):
            overlap = (circle1.radius + circle2.radius) - distance

            nx = dx / distance
            ny = dy / distance

            circle1.init_position[0] += nx * overlap / 2
            circle1.init_position[1] += ny * overlap / 2
            circle2.init_position[0] -= nx * overlap / 2
            circle2.init_position[1] -= ny * overlap / 2

            relative_velocity_x = circle1.x_velocity - circle2.x_velocity
            relative_velocity_y = circle1.y_velocity - circle2.y_velocity

            dot_product = relative_velocity_x * nx + relative_velocity_y * ny

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

                if abs(circle1.x_velocity) < circle1.friction:
                    circle1.x_velocity = 0
                if abs(circle1.y_velocity) < circle1.friction:
                    circle1.y_velocity = 0
                if abs(circle2.x_velocity) < circle2.friction:
                    circle2.x_velocity = 0
                if abs(circle2.y_velocity) < circle2.friction:
                    circle2.y_velocity = 0


class MixedCollision:
    @staticmethod
    def check_circle_square_collision(circle, square):
        """Check collision between a circle and a square."""
        cx, cy = circle.init_position
        radius = circle.radius

        left = square.rect.left
        right = square.rect.right
        top = square.rect.top
        bottom = square.rect.bottom

        nearest_x = max(left, min(cx, right))
        nearest_y = max(top, min(cy, bottom))

        dx = cx - nearest_x
        dy = cy - nearest_y
        distance = math.sqrt(dx**2 + dy**2)
        return distance < radius
    

    @staticmethod
    def resolve_circle_square_collision(circle, square):
        nearest_x = max(square.rect.left, min(circle.init_position[0], square.rect.right))
        nearest_y = max(square.rect.top, min(circle.init_position[1], square.rect.bottom))

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
