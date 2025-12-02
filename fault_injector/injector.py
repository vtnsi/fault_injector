# -*- coding: utf-8 -*-
"""
fault injector class
"""



class Injector:
    
    def __init__(self, fault, params = None):
        
        # TODO: add check for fault type
        self.fault = fault
        
        # TODO: add function to setup default params
        self.start = params['start']
        self.stop = params['stop']
        
        
    def inject_fault(self, x):
        f = self.fault(x[self.start:self.stop])
        x[self.start:self.stop] = f
        return x