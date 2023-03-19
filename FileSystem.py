import json
import os


class FileSystem():
    """
        Class for saving and loading using JSON files.
    """
    def __init__(self, file_path, file_extension = "json"):
        self.file_path = file_path
        self.file_extension = file_extension
    
    def save(self, data, file_name: str, indent = 2, cls = None):
        """
        Save [file_name] to the system

        Args:
            data: The data to be saved
            file_name: Name of the file
            indent: Indentation level of the JSON file
            cls: Class encoder when when encoding complex data
        """
        with open(self.get_full_path(file_name), "w") as file:
            json.dump(data, file, indent = indent, cls = cls)
    
    def load(self, file_name):
        """
        Load [file_name] from the system
        """
        if self.is_file_exist(file_name):
            with open(self.get_full_path(file_name), "r") as file:
                return json.load(file)
        else:
            return None
    
    def get_full_path(self, file_name):
        """
         Return the full path of [file_name] based on the file_path saved on the class
        """
        return os.path.join(self.file_path, file_name + "." + self.file_extension)
    
    def is_file_exist(self, file_name):
        """
        Check if [file_name] exists on the system
        """
        return os.path.exists(self.get_full_path(file_name)) \
            and os.path.isfile(self.get_full_path(file_name))