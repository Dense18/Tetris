import pygame

from ButtonObserver import ButtonObserver


class Button(ButtonObserver):
    """
        Creates a Button Widget inside a State Class
    """
    def __init__(self, state, x, y, width, height, 
                 text = "", textSize = 50, textColor = (255,255,255),
                 color = (0,0,0), hoverColor = (255,0,0),
                 borderRadius = 12, tag = ""):
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
        self.textFont = pygame.font.SysFont("cambria", 50)
        self.textColor = textColor
        self.text = self.textFont.render(text, 1, self.textColor)
        self.textRect = self.text.get_rect(center = self.rect.center)

        self.tag = tag
        self.pressed = False
        self.has_hovered = False
        self.onClickListener = None
        self.OnFirstHoverListener = None
        self.onHoverListener = None
        self.onButtonDownListener = None


    def setOnClickListener(self, listener):
        self.onClickListener = listener
    
    def setOnHoverListener(self, listener):
        self.onHoverListener = listener
    
    def setOnFirstHoverListener(self, listener):
        self.OnFirstHoverListener= listener
    
    def setOnButtonDownListener(self, listener):
        self.onButtonDownListener = listener

    def update(self, position, mouseEvent):
        if self.rect.collidepoint(position):
            self.currentColor = self.hoverColor
            if self.onHoverListener: self.onHoverListener()
            if not self.has_hovered:
                self.has_hovered = True
                if self.onHoverListener: self.onHoverListener(self, True)
            else:
                if self.onHoverListener: self.onHoverListener(self, False)
            if mouseEvent[0]: ##Left Click
                if not self.pressed and self.onButtonDownListener: self.onButtonDownListener()
                self.pressed = True
            else:
                if self.pressed:
                    if (self.onClickListener != None): self.onClickListener(self)
                    self.pressed = False        
        else:
            self.has_hovered = False
            self.currentColor = self.color

    def draw(self, screen):
        pygame.draw.rect(screen, self.currentColor, self.rect, border_radius = self.borderRadius)
        screen.blit(self.text, self.textRect)