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
    

class TetrisInformationEncoder(json.JSONEncoder):
    def default(self, obj):
        return {
            "__meta": "_TetrisInformation",
            "Level": obj.level,
            "Score": obj.score,
            "Lines Cleared": obj.lines_cleared,
            "Time Passed": obj.time_passed,
            "Game Mode": obj.game_mode
        }
        
        