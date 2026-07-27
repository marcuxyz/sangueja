from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def perform(self):
        print("chamou pai")
        raise NotImplementedError("Can't instantiate abstract class")
