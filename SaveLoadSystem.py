import json
import os


class SaveLoadSystem():
    """
        Class for saving and loading a file
    """
    def __init__(self, file_path, file_extension = "json"):
        self.file_path = file_path
        self.file_extension = file_extension
    
    def save(self, data, file_name, indent = 2, cls = None):
        with open(self.get_full_path(file_name), "w") as file:
            json.dump(data, file, indent = indent, cls = cls)
    
    def load(self, file_name):
        if self.is_file_exist(file_name):
            with open(self.get_full_path(file_name), "r") as file:
                return json.load(file)
        else:
            return None
    
    def get_full_path(self, file_name):
        return os.path.join(self.file_path, file_name + "." + self.file_extension)
    
    def is_file_exist(self, file_name):
        return os.path.exists(self.get_full_path(file_name)) \
            and os.path.isfile(self.get_full_path(file_name))