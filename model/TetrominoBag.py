import random
from collections.abc import MutableMapping, MutableSequence

from model.Tetromino import Tetromino


class TetrominoBag(MutableSequence):
    def __init__(self, min_item):
        super(TetrominoBag, self).__init__()
        self.shape_list = []
        self.min_item = min_item
        self.check_bag()
        
    def _add_new_bag(self):
        self += random.sample(list(Tetromino.SHAPE.keys()), len(Tetromino.SHAPE.keys()))
        print(f"bag item = {len(self)}")
    
    def check_bag(self):
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





        
