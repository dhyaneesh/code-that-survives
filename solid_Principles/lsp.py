# Bad Design (LSP Violation)
class Bird:
    def fly(self):
        pass

class Ostrich(Bird):
    def fly(self):
        raise Exception("I can't fly!")  # Breaks substitution


# Good Design (LSP Compliant)
class Bird:
    pass

class FlyingBird(Bird):
    def fly(self):
        pass

class Sparrow(FlyingBird):
    def fly(self):
        return "Flying..."

class Ostrich(Bird):
    pass
