# -*- coding: utf-8 -*-
"""
fault injector class
"""
import numpy as np
from numbers import Number
from numpy.typing import ArrayLike


class Injector:
    """
    Class designed to help generate and inject faults into data

    Args:
        fault : _description_
        params (dict, optional): params should include the start and stop keys. These values default to:
            - start (int): this corresponds to the starting index for the fault. defaults to 0.
            - stop (int): this corresponds to the ending index for the fault. defaults to -1.
    """

    def __init__(self, fault, params:dict = None):

        self.fault = fault

        if params is None:
            # set default values for params
            params = {'start': 0,
                      'stop': -1}

        if params.get('start') is None:
            params['start'] = 0

        if params.get('stop') is None:
            params['stop'] = -1

        self.start = params.get('start')
        self.stop = params.get('stop')
        self._initial_check_params()


    def inject_fault(self, x:ArrayLike) -> np.ndarray:
        """
        Inject the fault into the data

        Args:
            x (ArrayLike): the original values that will get the fault injected into it

        Returns:
            np.ndarray: the updated values after the fault is injected into it
        """
        x = self._check_data_type(x)
        self._check_params(x)

        x = x.copy()
        f = self.fault(x[self.start:self.stop])
        x[self.start:self.stop] = f
        return x


    def check_fault_instance(self, fault):
        """
        Check that fault is a fault class instance

        Args:
            fault: fault variable used during initialization

        Raises:
            TypeError: _description_
        """
        if isinstance(fault, type):
            raise TypeError("Expected a fault instance, not a class. \n For example: fault=MyFaultClass(params)")


    def _initial_check_params(self):
        """
        Checks the params
        - start: must be an int value
        - stop: must be an int value

        Raises:
            ValueError: param is None
            ValueError: param needs to be an int value
        """
        # start checks
        if self.start is None:
            raise ValueError(f"Invalid 'start': \n self.start is set to none")
        elif not isinstance(self.start, (int, np.int64, np.int32)):
            raise ValueError(f"Invalid 'start': \n must be an int type (int, np.int64, np.int32).")

        # stop checks
        if self.stop is None:
            raise ValueError(f"Invalid 'stop': \n self.stop is set to none")
        elif not isinstance(self.stop, (int, np.int64, np.int32)):
            raise ValueError(f"Invalid 'stop': \n must be an int type (int, np.int64, np.int32).")


    def _check_data_type(self, x:ArrayLike):
        """
        Check that x is an array containing numeric values

        Args:
            x (ArrayLike): array containing numeric values that represent the original value

        Raises:
            ValueError: 'x' must be an array
            ValueError: 'x' must contain numeric values

        """

        if not isinstance(x, (list, tuple, np.ndarray)):
            raise ValueError(
                "Invalid 'x': must be array-like (list, tuple, np.ndarray)"
            )

        x = np.asarray(x)

        if not np.issubdtype(x.dtype, np.number):
            raise ValueError(f"Invalid 'x': \n must contain numeric values")

        return x


    def _check_params(self, x):
        """
        Checks the params
        - start: must be an int value between [-len(x):len(x)]
        - stop: must be an int value between [-len(x)+1:len(x)+1]

        Raises:
            ValueError: param is outside index range
        """
        self._initial_check_params()
        x_len = len(x)

        # start checks
        if self.start >= x_len:
            raise ValueError(f"Invalid 'start': \n the current start value is outside the x index values \n current start={self.start}, length of x={x_len}")
        elif self.start < -x_len:
            raise ValueError(f"Invalid 'start': \n the current start value is outside the x index values \n current start={self.start}, length of x={x_len}")

        # stop checks
        if self.stop > x_len:
            raise ValueError(f"Invalid 'stop': \n the current stop value is outside the x index values \n current stop={self.stop}, length of x={x_len}")
        elif self.stop <= -x_len:
            raise ValueError(f"Invalid 'stop': \n the current stop value is outside the x index values \n current stop={self.stop}, length of x={x_len}")

