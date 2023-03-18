import pygame

from settings import *


class PlayMenuUI:
    def __init__(self, menu_state):
        self.menu_state = menu_state
        
        self.font = pygame.font.SysFont("Arial", HINT_TEXT_SIZE)
        self.marathon_hint_flag, self.zen_hint_flag, self.sprint_hint_flag, self.ultra_hint_flag = False, False, False, False
        
    def draw(self):
        self.draw_buttons()
        if self.marathon_hint_flag:
            self.draw_marathon_hint()
        if self.zen_hint_flag:
            self.draw_zen_hint()
        if self.sprint_hint_flag:
            self.draw_sprint_hint()
        if self.ultra_hint_flag:
            self.draw_ultra_hint()
        self.marathon_hint_flag, self.zen_hint_flag, self.sprint_hint_flag, self.ultra_hint_flag = False, False, False, False
        
    def draw_buttons(self):
        for button in self.menu_state.button_list: button.draw(self.menu_state.app.screen)
    
    def draw_marathon_hint(self):
        self.marathon_hint_flag = True
        button_rect = self.menu_state.marathon_button.original_elevated_rect
        
        text_obj = self.font.render("Get the highest score possible over a series of levels", 1, "white")
        text_obj_rect = text_obj.get_rect(x = button_rect.right + 20, centery = button_rect.centery)
        # bg_rect = pygame.Rect(centre = text_obj_rect)
        # pygame.draw.rect(self.menu_state.app.screen, (40,40,40), (text_obj_rect.x, text_obj_rect.y, button_rect.width,button_rect.height))
        self.menu_state.app.screen.blit(text_obj, text_obj_rect)

    def draw_zen_hint(self):
        self.zen_hint_flag = True
        button_rect = self.menu_state.zen_button.original_elevated_rect
        
        text_obj = self.font.render("Practice your skills with the neverending tetris mode", 1, "white")
        text_obj_rect = text_obj.get_rect(x = button_rect.right + 20, centery = button_rect.centery)
        self.menu_state.app.screen.blit(text_obj, text_obj_rect)
        
    def draw_sprint_hint(self):
        self.sprint_hint_flag = True
        button_rect = self.menu_state.sprint_button.original_elevated_rect
        
        text_obj = self.font.render(f"Clear {SPRINT_LINE_TO_CLEAR} lines quickly", 1, "white")
        text_obj_rect = text_obj.get_rect(x = button_rect.right + 20, centery = button_rect.centery)
        self.menu_state.app.screen.blit(text_obj, text_obj_rect)
    
    def draw_ultra_hint(self):
        self.ultra_hint_flag = True
        button_rect = self.menu_state.ultra_button.original_elevated_rect
        
        text_obj = self.font.render("Clear as many lines as possible within the time frame", 1, "white")
        text_obj_rect = text_obj.get_rect(x = button_rect.right + 20, centery = button_rect.centery)
        self.menu_state.app.screen.blit(text_obj, text_obj_rect)


        
        
        
        