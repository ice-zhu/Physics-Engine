from enum import Enum

"""Enum class to differentiate the different primitive shapes. Primarily used for collision detection."""
class ShapeType(Enum):
    CIRCLE = 1
    SQUARE = 2