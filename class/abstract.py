from abc import ABC, abstractmethod

class RemoteControl(ABC):
    @abstractmethod
    def toggle_power(self):
        pass

class TVRemote(RemoteControl):
    def toggle_power(self):
        return "TV is now ON"

remote = TVRemote()
print(remote.toggle_power())