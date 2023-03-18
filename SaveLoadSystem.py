import json
import os


class SaveLoadSystem():
    def __init__(self, file_path, file_extension = "json"):
        self.file_path = file_path
        self.file_extension = file_extension
    
    def save(self, data, file_name):
        with open(self.get_full_path(file_name), "w") as file:
            json.dump(data, file)
    
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