# -*- coding: utf-8 -*-
"""
offset fault class
"""
import numpy as np
import pandas as pd
from fault_injector.fault_lib.base_fault import BaseFault


class OffsetFault(BaseFault):
    r"""
    Offset Fault
    ============
    A fault type that adds a constant bias to all input values. This models
    sensor bias, calibration drift, or a persistent measurement error where
    values remain accurate in trend but are systematically shifted.

    The offset is specified directly through ``offset_by``, which represents
    the amount added to each input element.

    .. admonition:: Mathematical Definition

        For an input sequence :math:`x_i`, the offset fault produces:

        .. math::

            y_i = x_i + b

        where:

        - :math:`b` = ``offset_by`` (the constant additive bias)
        - :math:`y_i` = faulted values returned by :meth:`__call__`

        **Impact on Statistical Properties**

        - **Mean shift:**

          Adding a constant offset increases the mean by exactly that amount:

          .. math::

              \bar{y} = \bar{x} + b

        - **Variance unchanged:**

          Because variance measures spread, a constant shift does not affect it:

          .. math::

              \mathrm{Var}(y) = \mathrm{Var}(x)

        Offset faults therefore preserve the distribution's shape while shifting
        its central tendency.

    Notes
    -----
    Offset faults commonly model:

    - sensor bias or miscalibration
    - ADC offset
    - thermal drift-induced baseline shifts
    - constant noise floor elevation
    """
    def __init__(self, offset_by):
        """
        Initialize the OffsetFault.

        Parameters
        ----------
        offset_by : float
            Constant additive bias applied to every input value. This value
            may be positive or negative, producing an upward or downward shift.

        Notes
        -----
        The offset magnitude is applied uniformly across the full length of
        any array provided to :meth:`__call__`.
        """
        name = 'offset fault'
        super().__init__(name=name)
        super()._check_numeric_input(offset_by, 'offset_by')

        self.offset_by = offset_by


    def __call__(self, x, list_output=False):
        r"""
        Apply the offset fault to an input sequence or generate a zero-valued
        sequence to offset.

        Parameters
        ----------
        x : int, list, or numpy.ndarray
            - If ``int``: creates a zero array of length ``x`` and applies the offset.
            - If list or ndarray: each element receives ``offset_by``.

        list_output : bool, optional
            If ``True``, output is returned as a Python list; otherwise an
            ndarray and the internal fault state are updated.

        Returns
        -------
        numpy.ndarray or list
            The offset fault values :math:`y_i = x_i + b`.

        Notes
        -----
        The operation is elementwise and preserves the structure of the input.
        """
        if isinstance(x, int):
            x = super().create_zeros_array(x)

        super()._check_list_array(x, 'x')

        if isinstance(x, list):
            fault_values = list(map(lambda a: a + self.offset_by, x))
            list_output = True
        else:
            fault_values = x + self.offset_by

        if list_output:
            return super()._list_output(fault_values)
        super().update_fault(fault_values)
        return self.fault_values