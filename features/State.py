from abc import ABC, abstractmethod
class State(ABC):
    """
        Abstract Interface of each State of the Game
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def update(self, events):
        pass

    @abstractmethod    
    def draw(self):
        pass
