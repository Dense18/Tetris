from FileSystem import FileSystem
from model.TetrisStat import TetrisStat, TetrisStatEncoder
from settings import *


class TetrisStatFileManager:
    def __init__(self):
        self.file_system = FileSystem("", "json")
        
    def get_data(self) -> dict:
        """
            Returns a dict containing the best tetris stats.
        """
        data = self.file_system.load(BEST_SCORE_FILE_NAME)
        return data if data else {
            "__meta": "_GameMode"
        }
    
    def clear_data(self) -> dict:
        """
            Clear all the data on the saved best TetrisState file 
        """
        self.save_dict({})
        
    def save_dict(self, tetris_stat_dict):
        """
        Save [tetris_stat_dict] to the system
        """
        self.file_system.save(tetris_stat_dict, BEST_SCORE_FILE_NAME, cls = TetrisStatEncoder)
    
    # def save(self, tetris_info: TetrisStat):
    #     """
    #     Save [tetris_info] to the system
    #     """
    #     self.file_system.save(BEST_SCORE_FILE_NAME, tetris_info)
        