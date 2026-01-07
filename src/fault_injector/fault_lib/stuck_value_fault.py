# -*- coding: utf-8 -*-
"""
stuck value fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number
from numpy.typing import ArrayLike


class StuckValueFault(BaseFault):
    """
    Simulate a stuck value by repeating the stuck value for the desired length of values.

    Args:
        params (dict, optional): dictionary containing the `stuck_val` key, which corresponds to the repeated value in the output. If set to None, defaults to a `stuck_val` of 1.
    """
    def __init__(self, params:dict = None):
        self.name = 'stuck_value_fault'

        if params is None:
            # set default values for params
            params = {'stuck_val': 1}

        self.stuck_val = params.get('stuck_val')
        self._check_params()


    def __call__(self, x:ArrayLike)->np.ndarray:
        """The call method generates the stuck value fault

        Args:
            x (ArrayLike): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the altered values
        """
        self._check_params()
        x = self._check_data_type(x)

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
