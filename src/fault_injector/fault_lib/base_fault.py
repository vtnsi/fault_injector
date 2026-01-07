# -*- coding: utf-8 -*-
"""
base fault class
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import ArrayLike


class BaseFault:
    """
    BaseFault
    ---------

    """
    def __init__(self):

        self.name = 'base_fault'


    def __call__(self, x):

        return x

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