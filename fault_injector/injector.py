# -*- coding: utf-8 -*-
"""
fault injector class
"""



class Injector:
    
    def __init__(self, x, params = None):
        
        # TODO: add check for input
        self.x = x
        
        # TODO: add function to setup default params
        self.start = params['start']
        self.stop = params['stop']
        
        
    def inject_fault(self, fault):
        f = fault(self.x[self.start:self.stop])
        y = self.x.copy()
        y[self.start:self.stop] = f
        return y