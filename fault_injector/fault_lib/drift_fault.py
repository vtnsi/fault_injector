# -*- coding: utf-8 -*-
"""
drift fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault


class DriftFault(BaseFault):
    def __init__(self, params):
        r"""
        DriftFault
        ----------

        """
        self.name = 'drift_fault'
        
        # TODO: add checks for parameter type
        self.drift_rate = params['drift_rate']


    def __call__(self, x):
        
        # TODO:  add data type check
        
        drift = np.arange(1, len(x)+1)*self.drift_rate
        return x + drift

    
    def _check_params(self):
        pass
    
    
    def _check_data_type(self):
        pass