import json


class TetrisInformation(json.JSONEncoder):
    """
        Class to store tetris information when game has ended
    """
    def __init__(self, level, score, lines_cleared, time_passed, game_mode) -> None:
        self.level = level
        self.score = score
        self.lines_cleared = lines_cleared
        self.time_passed = time_passed
        self.game_mode = game_mode
    
    def default(self, obj):
        # return {
        #     self.game_mode:{
        #         "Level": obj.level,
        #         "Score": obj.score,
        #         "Lines Cleared": obj.lines_cleared,
        #         "Time Passed": obj.time_passed
        #     }
        # }
        
        
        return {
            obj.game_mode: obj.score
        }