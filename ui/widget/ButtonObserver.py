from abc import ABC, abstractmethod


class ButtonObserver(ABC):
    """
    Interface for button observers.
    """
    @abstractmethod
    def update(self, mouse_position, mouse_pressed):
        raise NotImplementedError