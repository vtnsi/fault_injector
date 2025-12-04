# -*- coding: utf-8 -*-
"""
offset fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number

class OffsetFault(BaseFault):
    def __init__(self, params:dict = None):
        r"""
        OffsetFault
        ----------

        Args
        ----
        params (dict):
        - offset_by (numeric):

        """
        self.name = 'offset_fault'

        if params is None:
            # set default values for params
            params = {'offset_by': 1}

        self.offset_by = params.get('offset_by')
        self._check_params()


    def __call__(self, x:np.array)->np.ndarray:
        """The call method generates the offset fault

        Args:
            x (np.array): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the altered values
        """
        self._check_params()
        self._check_data_type(x)

        return x + self.offset_by


    def _check_params(self):
        """
        Checks the params
        - offset_by: must be numeric

        Raises:
            ValueError: offset_by is None
            ValueError: offset_by needs to be a numeric value
        """
        if self.offset_by is None:
            raise ValueError(f"Invalid 'offset_by': \n no offset_by set in params")

        elif not isinstance(self.offset_by, (Number, np.number)):
            raise ValueError(f"Invalid 'offset_by': \n must be a numeric type (float, int, np.int64, np.float32, np.float64, np.int32, etc.).")


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
