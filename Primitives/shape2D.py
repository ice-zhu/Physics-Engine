from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def apply(self, mouse_cPos):
        pass

    @abstractmethod
    def draw(self, screen):
        pass
