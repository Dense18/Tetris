from abc import ABC, abstractmethod


class State(ABC):
    """
        Abstract Interface of each State of the Game
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def update(self, events):
        """
            Update state in each frame 
            
            Args:
                events: list of pygame events
        """
        pass

    @abstractmethod    
    def draw(self):
        """
            Draw the current state onto the screen
        """
        pass
