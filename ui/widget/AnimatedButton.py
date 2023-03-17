import pygame

from ui.widget.Button import Button


class AnimatedButton(Button):
    """
        Button with animated functionality
    """
    def __init__(self, state, x, y, width, height, 
                 text = "", textSize = 50, textColor = (255,255,255),
                 color = (0,0,0), hoverColor = (255,0,0),
                 borderRadius = 12):
        super().__init__(state, x, y, width, height, text, textSize, textColor, color, hoverColor, borderRadius)
        self.elevation = 20
        self.dynamicElevation = self.elevation

        self.bottomRect = pygame.Rect((self.x, self.y), (self.width, self.elevation))
        self.bottomRectColor = "#354b5E"

    def update(self, position, mouseEvent):
        if self.rect.collidepoint(position):
            self.currentColor = self.hoverColor
            if not self.has_hovered:
                self.has_hovered = True
                if self.onHoverListener: self.onHoverListener()
            if mouseEvent[0]: ##Left Click
                self.dynamicElevation = 0
                self.pressed = True
            else:
                self.dynamicElevation = self.elevation
                if self.pressed:
                    if (self.onClickListener != None): self.onClickListener()
                    self.pressed = False        
        else:
            self.has_hovered = False
            self.dynamicElevation = self.elevation
            self.currentColor = self.color
    
    def draw(self, screen):
        #Elevation
        self.rect.y = self.originalY - self.dynamicElevation
        self.textRect.center = self.rect.center
        self.bottomRect.midtop = self.rect.midtop
        self.bottomRect.height = self.rect.height + self.dynamicElevation
        pygame.draw.rect(screen, self.bottomRectColor, self.bottomRect, border_radius = self.borderRadius)

        super().draw(screen)