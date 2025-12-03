# -*- coding: utf-8 -*-
"""
NaN fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number

class NaNFault(BaseFault):
    def __init__(self):
        r"""
        NaNFault
        ----------

        Args
        ----
        None

        """
        self.name = 'nan_fault'


    def __call__(self, x:np.array)->np.ndarray:
        """The call method generates the NaN fault

        Args:
            x (np.array): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the NaN values
        """
        self._check_data_type(x)

        return np.full(len(x), np.nan)


    def _check_data_type(self, x:np.array):
        """
        Check that x is an array containing numeric values

        Args:
            x (np.ndarray): array containing numeric values that represent the original value

        Raises:
            ValueError: 'x' must be an array
            ValueError: 'x' must contain numeric values

        """

        if not isinstance(x, np.ndarray):
            raise ValueError(f"Invalid 'x': \n must be an np.ndarray")
        elif not np.issubdtype(x.dtype, np.number):
            raise ValueError(f"Invalid 'x': \n must contain numeric values")
