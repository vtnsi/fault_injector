# -*- coding: utf-8 -*-
"""
uniform noise fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number
from numpy.typing import ArrayLike


class UniformNoiseFault(BaseFault):
    def __init__(self, params:dict = None):
        r"""
        UniformNoiseFault
        ----------

        Args
        ----
        params (dict):
        - min_val (numeric): Mean of the Gaussian noise distribution
        - max_val (numeric): Standard deviation of the Gaussian noise distribution. Must be non-negative.


        """
        self.name = 'uniform_noise_fault'

        if params is None:
            # set default values for params
            params = {'min_val': 0,
                      'max_val': 1}

        self.min_val = params.get('min_val')
        self.max_val = params.get('max_val')
        self._check_params()


    def __call__(self, x:ArrayLike)->np.ndarray:
        """The call method generates the uniform noise fault

        Args:
            x (ArrayLike): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the altered values
        """
        self._check_params()
        x = self._check_data_type(x)

        noise =  np.random.uniform(self.min_val, self.max_val, len(x))
        return x + noise


    def _check_params(self):
        """
        Checks the params
        - min_val: must be numeric
        - max_val: must be numeric

        Raises:
            ValueError: param is None
            ValueError: param needs to be a numeric value
        """
        # min_val checks
        if self.min_val is None:
            raise ValueError(f"Invalid 'min_val': \n no min_val set in params")
        elif not isinstance(self.min_val, (Number, np.number)):
            raise ValueError(f"Invalid 'min_val': \n must be a numeric type (float, int, np.int64, np.float32, np.float64, np.int32, etc.).")

        # max_val checks
        if self.max_val is None:
            raise ValueError(f"Invalid 'max_val': \n no max_val set in params")
        elif not isinstance(self.max_val, (Number, np.number)):
            raise ValueError(f"Invalid 'max_val': \n must be a numeric type (float, int, np.int64, np.float32, np.float64, np.int32, etc.).")
        elif self.max_val <= self.min_val:
            raise ValueError(f"Invalid 'max_val': \n must be greater than min_val")
