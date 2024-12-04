class Collision:
    """To deal with collision among other objects primarily."""

    @staticmethod
    def check_collision(square1, square2):
        """Check if two squares are colliding."""
        if square1.rect.colliderect(square2.rect):
            square1.color = (255, 0, 0)  # Change color when colliding
        return square1.rect.colliderect(square2.rect)

    @staticmethod
    def resolve_collision(square1, square2):
        """Resolve the collision between two squares."""
        overlap_x = min(square1.rect.right, square2.rect.right) - max(square1.rect.left, square2.rect.left)
        overlap_y = min(square1.rect.bottom, square2.rect.bottom) - max(square1.rect.top, square2.rect.top)

        # If there is overlap (i.e., a collision), handle it
        if overlap_x > 0 and overlap_y > 0:
            # Resolve the collision by determining which axis has the smaller overlap
            if overlap_x < overlap_y:
                if square1.rect.centerx < square2.rect.centerx:
                    # Move square1 left to resolve horizontal collision
                    square1.rect.right -= overlap_x
                    square2.rect.left = square1.rect.right  # Ensure square2 stays correctly aligned
                    square1.x_velocity *= -1 * square1.retention  # Invert x velocity with retention
                    if abs(square1.x_velocity) < square1.gravity.bounce_stop:
                        square1.x_velocity = 0  # Stop movement if velocity is too small
                else:
                    # Move square1 right to resolve horizontal collision
                    square1.rect.left += overlap_x
                    square2.rect.right = square1.rect.left  # Ensure square2 stays correctly aligned
                    square1.x_velocity *= -1 * square1.retention  # Invert x velocity with retention
                    if abs(square1.x_velocity) < square1.gravity.bounce_stop:
                        square1.x_velocity = 0  # Stop movement if velocity is too small
            else:
                if square1.rect.centery < square2.rect.centery:
                    # Move square1 up to resolve vertical collision
                    square1.rect.bottom -= overlap_y
                    square2.rect.top = square1.rect.bottom  # Ensure square2 stays correctly aligned
                    square1.y_velocity *= -1 * square1.retention  # Invert y velocity with retention
                    if abs(square1.y_velocity) < square1.gravity.bounce_stop:
                        square1.y_velocity = 0  # Stop movement if velocity is too small
                else:
                    # Move square1 down to resolve vertical collision
                    square1.rect.top += overlap_y
                    square2.rect.bottom = square1.rect.top  # Ensure square2 stays correctly aligned
                    square1.y_velocity *= -1 * square1.retention  # Invert y velocity with retention
                    if abs(square1.y_velocity) < square1.gravity.bounce_stop:
                        square1.y_velocity = 0  # Stop movement if velocity is too small

            # Ensure the squares no longer overlap by fixing their velocities and positions
            # Prevent squares from sticking after the collision
            if abs(square1.x_velocity) < square1.gravity.bounce_stop:
                square1.x_velocity = 0  # Stop horizontal velocity if it's too small
                square1.init_position[0] = square1.rect.x  # Update initial position to prevent sticking

            if abs(square1.y_velocity) < square1.gravity.bounce_stop:
                square1.y_velocity = 0  # Stop vertical velocity if it's too small
                square1.init_position[1] = square1.rect.y-square2.rect.y  # Update initial position to prevent sticking

