# -*- coding: utf-8 -*-
"""
normal noise fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number
from numpy.typing import ArrayLike

class NormalNoiseFault(BaseFault):
    """
    Simulates a normal (gaussian) noise fault

    Args:
        params (dict, optional):
            - mu (numeric): Mean of the Gaussian noise distribution
            - sigma (numeric): Standard deviation of the Gaussian noise distribution. Must be non-negative.
    """
    def __init__(self, params:dict = None):
        self.name = 'normal_noise_fault'

        if params is None:
            # set default values for params
            params = {'mu': 0,
                      'sigma': 1}

        self.mu = params.get('mu')
        self.sigma = params.get('sigma')
        self._check_params()


    def __call__(self, x:ArrayLike)->np.ndarray:
        """The call method generates the normal noise fault

        Args:
            x (ArrayLike): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the altered values
        """
        self._check_params()
        x = self._check_data_type(x)

        noise =  np.random.normal(self.mu, self.sigma, len(x))
        return x + noise


    def _check_params(self):
        """
        Checks the params
        - mu: must be numeric
        - sigma: must be numeric

        Raises:
            ValueError: param is None
            ValueError: param needs to be a numeric value
        """
        # mu checks
        if self.mu is None:
            raise ValueError(f"Invalid 'mu': \n no mu set in params")
        elif not isinstance(self.mu, (Number, np.number)):
            raise ValueError(f"Invalid 'mu': \n must be a numeric type (float, int, np.int64, np.float32, np.float64, np.int32, etc.).")

        # sigma checks
        if self.sigma is None:
            raise ValueError(f"Invalid 'sigma': \n no sigma set in params")
        elif not isinstance(self.sigma, (Number, np.number)):
            raise ValueError(f"Invalid 'sigma': \n must be a numeric type (float, int, np.int64, np.float32, np.float64, np.int32, etc.).")
        elif self.sigma < 0:
            raise ValueError(f"Invalid 'sigma': \n must be greater than or equal to 0")

