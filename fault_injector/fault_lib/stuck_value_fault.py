# -*- coding: utf-8 -*-
"""
stuck value fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number

class StuckValueFault(BaseFault):
    def __init__(self, params:dict = None):
        r"""
        StuckValueFault
        ----------

        Args
        ----
        params (dict):
        - stuck_value (numeric):

        """
        self.name = 'stuck_value_fault'

        if params is None:
            # set default values for params
            params = {'stuck_val': 1}

        self.stuck_val = params.get('stuck_val')
        self._check_params()


    def __call__(self, x:np.array)->np.ndarray:
        """The call method generates the stuck value fault

        Args:
            x (np.array): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the altered values
        """
        self._check_params()
        self._check_data_type(x)

        return np.full(len(x), self.stuck_val)


    def _check_params(self):
        """
        Checks the params
        - stuck_val: must be numeric

        Raises:
            ValueError: stuck_val is None
            ValueError: stuck_val needs to be a numeric value
        """
        if self.stuck_val is None:
            raise ValueError(f"Invalid 'stuck_val': \n no stuck_val set in params")

        elif not isinstance(self.stuck_val, (Number, np.number)):
            raise ValueError(f"Invalid 'stuck_val': \n must be a numeric type (float, int, np.int64, np.float32, np.float64, np.int32, etc.).")


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
