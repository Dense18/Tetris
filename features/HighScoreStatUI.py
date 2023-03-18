class HighScoreStatUI:
    def __init__(self, high_score_state):
        self.state = high_score_state
        
    def draw(self):
        self.state.app.screen.fill("Black")