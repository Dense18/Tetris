import random
from collections.abc import MutableMapping, MutableSequence

from model.Tetromino import Tetromino


class TetrominoBag(MutableSequence):
    """
    Class handling the management of a bag of tetrominoes.
    """
    def __init__(self, min_item):
        """
            min_item: Minimum number of items in the bag befpre generating a new set of tetrominoes
        """
        super(TetrominoBag, self).__init__()
        self.shape_list = []
        self.min_item = min_item
        self.check_bag()
        
    def _add_new_bag(self):
        """
            Add a random permutation of Tetromino shapes to the current bag.
        """
        self += random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))
    
    def check_bag(self):
        """
            Checks and updates the bag if needed based on min_item.
        """
        if len(self) < self.min_item:
            self._add_new_bag()
    
    def __len__(self) -> int:
        return len(self.shape_list)
    
    def __setitem__(self, key, value):
        self.shape_list[key] = value
    
    def __getitem__(self, key):
        return self.shape_list[key]

    def __delitem__(self, index = -1):
        self.shape_list.__delitem__(index)
        self.check_bag()
    
    def insert(self, index, value) -> None:
        self.shape_list.insert(index, value)





        
