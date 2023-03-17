import json
import os


class SaveLoadSystem():
    def __init__(self, file_path):
        self.file_path = file_path
    
    def save(self, data, file_name):
        with open(os.path.join(self.file_path, file_name), "w") as file:
            json.dump(data, file)
    
    def load(self, file_name):
        if self.is_file_exist(file_name):
            with open(self.get_full_path(file_name), "r") as file:
                return json.load(file)
        else:
            return None
    
    def get_full_path(self, file_name):
        return os.path.join(self.file_path, file_name)
    
    def is_file_exist(self, file_name):
        return os.path.exists(self.get_full_path(file_name)) \
            and os.path.isfile(self.get_full_path(file_name))