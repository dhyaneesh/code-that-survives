
# BAD :# Adding a new shape means editing this function
def calculate_area(shape_type, value):
    if shape_type == "square":
        return value * value
    elif shape_type == "circle":
        return 3.14 * value * value



#Good: New shapes can be added without modifying existing functions
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * (self.radius ** 2)
