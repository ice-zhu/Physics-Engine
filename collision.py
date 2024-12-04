import math

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
        # Get the distance between the centers of the two circles
        dx = circle1.init_position[0] - circle2.init_position[0]
        dy = circle1.init_position[1] - circle2.init_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < (circle1.radius + circle2.radius):
            circle1.color = (255, 0, 0) #remove later
            return True
        return False

    @staticmethod
    def resolve_collision(circle1, circle2):
        """Resolve the collision between two circles."""
        dx = circle1.init_position[0] - circle2.init_position[0]
        dy = circle1.init_position[1] - circle2.init_position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < (circle1.radius + circle2.radius):
            # Calculate the overlap
            overlap = (circle1.radius + circle2.radius) - distance
            nx = dx / distance
            ny = dy / distance

            circle1.init_position[0] += nx * overlap / 2
            circle1.init_position[1] += ny * overlap / 2
            circle2.init_position[0] -= nx * overlap / 2
            circle2.init_position[1] -= ny * overlap / 2

            dot_product = (circle1.x_velocity * nx) + (circle1.y_velocity * ny)
            circle1.x_velocity -= 2 * dot_product * nx
            circle1.y_velocity -= 2 * dot_product * ny

            dot_product = (circle2.x_velocity * nx) + (circle2.y_velocity * ny)
            circle2.x_velocity -= 2 * dot_product * nx
            circle2.y_velocity -= 2 * dot_product * ny

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
