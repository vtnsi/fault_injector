# -*- coding: utf-8 -*-
"""
offset fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault
from numbers import Number
from numpy.typing import ArrayLike

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


    def __call__(self, x:ArrayLike)->np.ndarray:
        """The call method generates the offset fault

        Args:
            x (ArrayLike): array containing numeric values that represent the original value

        Returns:
            np.ndarray: array containing the altered values
        """
        self._check_params()
        x = self._check_data_type(x)

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

