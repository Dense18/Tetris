import pygame

from ButtonObserver import ButtonObserver


class Button(ButtonObserver):
    """
        Creates a Button Widget inside a State Class
    """
    def __init__(self, state, x, y, width, height, 
                 text = "", textSize = 50, textColor = (255,255,255),
                 color = (0,0,0), hoverColor = (255,0,0),
                 borderRadius = 12, image = None, tag = ""):
        self.state = state
        self.state.register(self)

        self.x = x
        self.y = y
        self.originalY = y
        self.width = width
        self.height = height

        self.color = color
        self.hoverColor = hoverColor
        self.currentColor = color
        
        self.borderRadius = borderRadius
        self.rect = pygame.Rect(self.x, self.y, width, height)

        self.textSize = textSize
        self.textFont = pygame.font.SysFont("cambria", self.textSize)
        self.textColor = textColor
        self.text = self.textFont.render(text, 1, self.textColor)
        self.textRect = self.text.get_rect(center = self.rect.center)
        
        self.image = pygame.transform.scale(image, (self.width * 0.8, self.height * 0.8)) if image is not None else None

        self.tag = tag
        self.pressed = False
        self.has_hovered = False
        self.onClickListener = None
        self.onHoverListener = None
        self.onButtonDownListener = None


    def setOnClickListener(self, listener):
        """
        [listener] is a function that will be called when the button is clicked.
        I.e, it will trigger when the button is released after it is pressed down.

        Args:
            listener(button): [button] is the current Button object. 
        """
        self.onClickListener = listener
    
    def setOnHoverListener(self, listener):
        """
        [listener] is a function that will be called when the button is hovered.
        I.e, when the mouse is over the button.

        Args:
            listener(button, first_hover: bool): [button] is the current Button object. 
            [first_hover] is True the first time the mouse hovers the button and False otherwise. It will reset when the mouse leaves the button 
        """
        self.onHoverListener = listener
    
    def setOnButtonDownListener(self, listener):
        """
        [listener] is a function that will be called when the button is pressed down.

        Args:
            listener(button): [button] is the current Button object. 
        """
        self.onButtonDownListener = listener

    def update(self, position, mouseEvent):
        """
        Updates the button based on the mouse position [position] and the mouse event [mouseEvent].
        """
        if self.rect.collidepoint(position):
            self.currentColor = self.hoverColor
            if not self.has_hovered:
                self.has_hovered = True
                if self.onHoverListener: self.onHoverListener(self, True)
            else:
                if self.onHoverListener: self.onHoverListener(self, False)
            if mouseEvent[0]: ##Left Click
                if not self.pressed and self.onButtonDownListener: self.onButtonDownListener(self)
                self.pressed = True
            else:
                if self.pressed:
                    if (self.onClickListener != None): self.onClickListener(self)
                    self.pressed = False        
        else:
            self.has_hovered = False
            self.currentColor = self.color

    def draw(self, screen):
        """Draws the button on the [screen].
        """
        pygame.draw.rect(screen, self.currentColor, self.rect, border_radius = self.borderRadius)
        screen.blit(self.text, self.textRect) if not self.image else screen.blit(self.image, self.textRect)