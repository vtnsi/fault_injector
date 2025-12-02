# -*- coding: utf-8 -*-
"""
dataframe fault injector
"""



class DataFrameInjector:
    
    def __init__(self, injector_dict):
        
        self.injector_dict = injector_dict
        
        
    def inject_faults(self, df):
        for col, f in self.injector_dict.items():
            df[col] = f.inject_fault(df[col].values)
        return df
            