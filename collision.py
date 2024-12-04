class Collision:
    """To deal with collision among other objects primarily."""

    @staticmethod
    def check_collision(square1, square2):
        """Check if two squares are colliding."""
        if square1.rect.colliderect(square2.rect):
            square1.color = (255, 0, 0)  
        return square1.rect.colliderect(square2.rect)

    @staticmethod
    def resolve_collision(square1, square2):
        """Resolve the collision between two squares."""
        overlap_x = min(square1.rect.right, square2.rect.right) - max(square1.rect.left, square2.rect.left)
        overlap_y = min(square1.rect.bottom, square2.rect.bottom) - max(square1.rect.top, square2.rect.top)

        if overlap_x > 0 or overlap_y > 0:
            if overlap_x < overlap_y:
                if square1.rect.centerx < square2.rect.centerx:
                    square1.rect.right -= overlap_x
                    square2.rect.left = square1.rect.right
                else:
                    square1.rect.left += overlap_x
                    square2.rect.right = square1.rect.left
            else:
                if square1.rect.centery < square2.rect.centery:
                    square1.rect.bottom -= overlap_y
                    square2.rect.top = square1.rect.bottom
                else:
                    square1.rect.top += overlap_y
                    square2.rect.bottom = square1.rect.top

            square1.x_velocity, square2.x_velocity = square2.x_velocity, square1.x_velocity
            square1.y_velocity, square2.y_velocity = square2.y_velocity, square1.y_velocity

