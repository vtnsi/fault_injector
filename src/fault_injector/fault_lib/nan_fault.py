# -*- coding: utf-8 -*-
"""
NaN fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number
from numpy.typing import ArrayLike

class NaNFault(BaseFault):
    """
    Simulate a **NaN fault**: models a sensor failure where readings are completely missing for a continuous period of time
    """
    def __init__(self):
        self.name = 'nan_fault'


    def __call__(self, x:ArrayLike)->np.ndarray:
        """The call method generates the NaN fault

        Args:
            x (np.array): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the NaN values
        """
        x = self._check_data_type(x)

        return np.full(len(x), np.nan)

