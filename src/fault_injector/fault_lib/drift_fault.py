# -*- coding: utf-8 -*-
"""
drift fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number
from numpy.typing import ArrayLike

class DriftFault(BaseFault):
    """
    Simulate a Drift Fault: a gradual, systematic deviation of sensor readings from their true values over time.

    Args:
        params (dict, optional): Dictionary containing the `drift_rate` key. `drift_rate` corresponds to the slope of the fault-induced offset. If None, defaults to `drift_rate` of 1.
    """
    def __init__(self, params:dict = None):
        self.name = 'drift_fault'

        if params is None:
            # set default values for params
            params = {'drift_rate': 1}

        self.drift_rate = params.get('drift_rate')
        self._check_params()


    def __call__(self, x:ArrayLike)->np.ndarray:
        """The call method generates the drift fault

        Args:
            x (np.array): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the altered values
        """
        self._check_params()
        x = self._check_data_type(x)

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

