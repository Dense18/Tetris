from abc import ABC, abstractmethod


class Subject(ABC):
    """
    Interface for subjects dealing with Button Observers
    """
    @abstractmethod
    def register(self, observer):
        raise NotImplementedError
    
    @abstractmethod
    def unregister(self, observer):
        raise NotImplementedError
    
    @abstractmethod
    def notify(self, mouse_position, mouse_pressed):
        raise NotImplementedError