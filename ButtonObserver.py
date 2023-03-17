from abc import ABC, abstractmethod


class ButtonObserver(ABC):
    
    @abstractmethod
    def update(self, mouse_position, mouse_pressed):
        raise NotImplementedError