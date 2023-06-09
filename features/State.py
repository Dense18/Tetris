from abc import ABC, abstractmethod

from features.Subject import Subject


class State(Subject, ABC):
    """
        Abstract Class of each State of the Game
    """
    
    ADD_STATE = 0
    """
    If set, add the state to the state stack.
    """

    CLEAR_TOP = 1
    """
    If set, and the state exists on the state stack, instead of creating a new state, all the other states on top of it will be exited and 
    the top of the state stack will then be the current state. Otherwise, if the state does not exist on the state stack, all the state on the state
    stack will be exited and the top of the state stack will be the current state.
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
    
    def start_state(self, state, flag = ADD_STATE):
        """
        Start a new state [state] to the application. Same as calling [state].enter_state(flag)
        
        Args:
            Flag: additional instruction when entering the state.
        """
        state.enter_state(flag)
    
    def enter_state(self, flag = ADD_STATE):
        """
        Enter the current state.

        Args:
            Flag: additional instruction when entering the state.
        """
        if flag == State.CLEAR_TOP:
            for i, state in enumerate(self.app.state_stack):
                if isinstance(state, self.__class__):
                    self.clear_top(i)
                    return
            self.clear_top(0)
            self.add_current_state()
        elif flag == State.ADD_STATE:
            self.add_current_state()
        else:
            raise ValueError("Invalid flag")
    
    def clear_top(self, stack_index):
        """
            Clear all state above the given [stack_index] in the state stack
        """
        for i in range(stack_index + 1, len(self.app.state_stack)):
            self.app.state_stack[-1].exit_state()
            
        if len(self.app.state_stack) > 1:
            self.prev_state = self.app.state_stack[-1]
            
    def add_current_state(self):
        """
            Append current state to the state stack
        """
        if len(self.app.state_stack) > 1:
            self.app.state_stack[-1].on_leave_state()
            self.prev_state = self.app.state_stack[-1]
        
        self.app.state_stack.append(self)
        self.app.state_stack[-1].on_start_state()
        self.app.state_stack[-1].on_resume_state()
    
    
    def on_start_state(self):
        """
            Called when state is first started
        """
        pass
        
    def on_resume_state(self):
        """
        Called when the state is resumed. Also called after on_start()   
        """
        pass
    
    def on_exit_state(self):
        """
        Called when the state is removed from the stack.        
        """
        pass
    
    def exit_state(self):
        """
            Exit the current state and pop it from the state stack
        """
        self.app.state_stack[-1].on_leave_state()
        self.app.state_stack[-1].on_exit_state()
        self.app.state_stack.pop()
        if len(self.app.state_stack): self.app.state_stack[-1].on_resume_state()
    
    
    def on_leave_state(self):
        """
        Called when leaving the state 
        """
        pass
    
    def register(self, observer):
        self.observer_list.append(observer)
    
    def unregister(self, observer):
        self.observer_list.remove(observer)
    
    def notify(self, mouse_position, mouse_pressed):
        for observer in self.observer_list:
            observer.update(mouse_position, mouse_pressed)
    
