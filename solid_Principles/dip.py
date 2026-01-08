# Bad Design
class Bulb:
    def turn_on(self):
        print("Bulb ON")

class Switch:
    def __init__(self):
        self.bulb = Bulb()   # Hard dependency

    def operate(self):
        self.bulb.turn_on()


# Good Design
class Switchable:
    def turn_on(self): pass

class Switch:
    def __init__(self, device):
        self.device = device

    def operate(self):
        self.device.turn_on()

class Fan(Switchable): ...
class Lamp(Switchable): ...
