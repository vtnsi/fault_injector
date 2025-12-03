# -*- coding: utf-8 -*-
"""
drift fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number

class DriftFault(BaseFault):
    def __init__(self, params:dict = None):
        r"""
        DriftFault
        ----------

        Args
        ----
        params (dict):

        """
        self.name = 'drift_fault'

        if params is None:
            # set default values for params
            params = {'drift_rate': 1}

        self.drift_rate = params.get('drift_rate')
        self._check_params()


    def __call__(self, x:np.array)->np.ndarray:
        """The call method generates the drift fault

        Args:
            x (np.array): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the altered values
        """
        self._check_params()
        self._check_data_type(x)

        drift = np.arange(start=1, stop=len(x)+1) * self.drift_rate
        return x + drift


    def _check_params(self):
        """
        Checks the params
        - drift_rate: must be numeric

        Raises:
            ValueError: drift_rate is None
            ValueError: drift_rate needs to be a numeric value
        """
        if self.drift_rate is None:
            raise ValueError(f"Invalid 'drift_rate': \n no drift_rate set in params")

        elif not isinstance(self.drift_rate, (Number, np.number)):
            raise ValueError(f"Invalid 'drift_rate': \n must be a numeric type (float, int, np.int64, np.float32, np.float64, np.int32, etc.).")


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
