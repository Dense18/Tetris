import pygame

from ui.widget.Button import Button


class AnimatedButton(Button):
    """
        Button with animated functionality
    """
    def __init__(self, state, x, y, width, height, 
                 text = "", textSize = 50, textColor = (255,255,255),
                 color = (0,0,0), hoverColor = (255,0,0),
                 borderRadius = 12, elevation = 20, image = None, tag = ""):
        super().__init__(state, x, y, width, height, text, textSize, textColor, color, hoverColor, borderRadius, image, tag)
        self.elevation = elevation
        self.dynamicElevation = self.elevation
        
        # Store the original rect position after the elevation has been applied.
        # This rect position is used to check for button clicks.
        self.original_elevated_rect = pygame.Rect(self.x, self.y - self.elevation, width, height)
        
        self.bottomRect = pygame.Rect((self.x, self.y), (self.width, self.elevation))
        self.bottomRectColor = "#354b5E"

    def update(self, position, mouseEvent):
        if self.original_elevated_rect.collidepoint(position):
            self.currentColor = self.hoverColor
            if not self.has_hovered:
                self.has_hovered = True
                if self.onHoverListener: self.onHoverListener(self, True)
            else:
                if self.onHoverListener: self.onHoverListener(self, False)
                
            if mouseEvent[0]: ##Left Click
                self.dynamicElevation = 0
                if not self.pressed and self.onButtonDownListener: self.onButtonDownListener(self)
                self.pressed = True
            else:
                self.dynamicElevation = self.elevation
                if self.pressed:
                    if (self.onClickListener != None): self.onClickListener(self)
                    self.pressed = False        
        else:
            self.pressed = False
            self.has_hovered = False
            self.dynamicElevation = self.elevation
            self.currentColor = self.color

        # Update the current rect position after applying the dynamic elevation 
        self.rect.y = self.originalY - self.dynamicElevation
        self.textRect.center = self.rect.center
        self.bottomRect.midtop = self.rect.midtop
        self.bottomRect.height = self.rect.height + self.dynamicElevation

    
    def draw(self, screen):
        pygame.draw.rect(screen, self.bottomRectColor, self.bottomRect, border_radius = self.borderRadius)

        super().draw(screen)