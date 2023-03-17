from abc import ABC, abstractmethod

from Subject import Subject


class State(Subject, ABC):
    """
        Abstract Class of each State of the Game
    """
    def __init__(self, app):
        self.app = app
        self.prev_state = None
        
        self.observer_list = []
    
    @abstractmethod
    def update(self, events):
        """
            Update state in each frame 
            
            Args:
                events: list of pygame events
        """
        raise NotImplementedError

    @abstractmethod    
    def draw(self):
        """
            Draw the current state onto the screen
        """
        raise NotImplementedError
    
    def enter_state(self):
        if len(self.app.state_stack) > 1:
            self.prev_state = self.app.state_stack[-1]
        self.app.state_stack.append(self)
    
    def register(self, observer):
        self.observer_list.append(observer)
    
    def unregister(self, observer):
        self.observer_list.remove(observer)
    
    def notify(self, mouse_position, mouse_pressed):
        for observer in self.observer_list:
            observer.update(mouse_position, mouse_pressed)
    
