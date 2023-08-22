#!/usr/bin/python3

from math import sqrt

class Point():
    ''' Class to present a point in decart coordinate '''
    def __init__(self, x=None, y=None):
        self.x, self.y = x, y
    
    def __getitem__(self, i):
        if i==0: return self.x
        if i==1: return self.y
        return None
    
    def __len__(self):
        return 2
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x==other.x and self.y==other.y
        return NotImplemented
    
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
    
    