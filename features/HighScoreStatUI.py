import features.Tetris as Tetris
from settings import *


class HighScoreStatUI:
    """
        Class handling UI element for the HighScoreStat State
    """
    def __init__(self, high_score_state):
        self.state = high_score_state
        
        self.text_font = pygame.font.SysFont("Arial", TEXT_SIZE)
        self.marathon_stat_rect, self.sprint_stat_rect, self.ultra_stat_rect = None, None, None
        
        ## The box is an imaginary border of containing mode("Marathon", "Sprint", "Ultra") + the stats below it
        self.box_padding = 10
        self.box_height = TEXT_SIZE * 2 + 10
        
        ## The margin between each boxes
        self.margin_top = (self.state.app.screen.get_height() - (self.box_height* 3)) / 4
        
    def draw(self):
        self.state.app.screen.fill("Black")
        self.draw_marathon_stats()
        self.draw_sprint_stats()
        self.draw_ultra_stats()
        
        self.draw_buttons()
    
    def draw_marathon_stats(self):
        score = 0 if Tetris.Tetris.MODE_MARATHON not in self.state.data.keys() \
            else self.state.data[Tetris.Tetris.MODE_MARATHON]["Score"]
            
        marathon_label_obj = self.text_font.render("Marathon", True, "Red")
        marathon_label_rect = marathon_label_obj.get_rect(centerx = self.state.app.screen.get_width()/2, 
                                                          centery = self.margin_top)
        self.state.app.screen.blit(marathon_label_obj, marathon_label_rect)
        
        score_obj = self.text_font.render(f"Best Score: {score}", True, "White")
        self.marathon_stat_rect = score_obj.get_rect(centerx = self.state.app.screen.get_width()//2, 
                                                     y = marathon_label_rect.bottom + self.box_padding)
        self.state.app.screen.blit(score_obj, self.marathon_stat_rect)
    
    def draw_sprint_stats(self):
        lines_cleared = 0 if Tetris.Tetris.MODE_SPRINT not in self.state.data.keys() \
            else self.state.data[Tetris.Tetris.MODE_SPRINT]["Score"]
        
        sprint_label_obj = self.text_font.render("Sprint", True, "Red")
        sprint_label_rect = sprint_label_obj.get_rect(centerx = self.state.app.screen.get_width()//2, 
                                                      y = self.marathon_stat_rect.bottom + self.margin_top)
        self.state.app.screen.blit(sprint_label_obj, sprint_label_rect)
        
        lines_cleared_obj = self.text_font.render(f"Best Score: {lines_cleared}", True, "White")
        self.sprint_stat_rect = lines_cleared_obj.get_rect(centerx = self.state.app.screen.get_width()//2, 
                                                           y = sprint_label_rect.bottom + self.box_padding)
        self.state.app.screen.blit(lines_cleared_obj, self.sprint_stat_rect)
    
    def draw_ultra_stats(self):
        time_passed = 0 if Tetris.Tetris.MODE_ULTRA not in self.state.data.keys() \
            else self.state.data[Tetris.Tetris.MODE_ULTRA]["Score"]
        
        ultra_label_obj = self.text_font.render("Ultra", True, "Red")
        ultra_label_rect = ultra_label_obj.get_rect(centerx = self.state.app.screen.get_width()//2, 
                                                    y = self.sprint_stat_rect.bottom + self.margin_top)
        self.state.app.screen.blit(ultra_label_obj, ultra_label_rect)
        
        time_passed_obj = self.text_font.render(f"Best Score: {time_passed}", True, "White")
        self.ultra_stat_rect = time_passed_obj.get_rect(centerx = self.state.app.screen.get_width()//2, 
                                                        y = ultra_label_rect.bottom + self.box_padding)
        self.state.app.screen.blit(time_passed_obj, self.ultra_stat_rect)
    
    def draw_buttons(self):
        for button in self.state.button_list: button.draw(self.state.app.screen)