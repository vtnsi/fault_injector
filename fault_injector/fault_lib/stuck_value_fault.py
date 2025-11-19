# -*- coding: utf-8 -*-
"""
stuck value fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault


class StuckValueFault(BaseFault):
    r"""
    Stuck Value Fault
    =================
    A fault type that replaces all values in the faulted region with a single
    constant output. This simulates *sensor freezing*, where a device stops
    updating and continuously reports the same reading regardless of true input.

    The stuck value is supplied directly through ``stuck_val``.

    .. admonition:: Mathematical Definition

        For input sequence :math:`x_i`, a stuck-value fault produces:

        .. math::

            y_i = c

        for all indices in the fault duration, where:

        - :math:`c` = ``stuck_val`` (constant output)
        - :math:`y_i` = faulted values returned by :meth:`__call__`

        **Impact on Statistical Properties**

        - **Mean collapse to constant:**

          .. math::

              \bar{y} = c

        - **Variance collapses to zero:**

          Because every value is identical,

          .. math::

              \mathrm{Var}(y) = 0

        Stuck-value faults therefore eliminate all dynamic information within the
        faulted window.

    Notes
    -----
    Stuck-value faults commonly represent:

    - frozen ADC readings
    - microcontroller hang states
    - communication deadlocks
    - sensor hardware failure where output holds its last value
    """
    def __init__(self, stuck_val):
        r"""
        Initialize the StuckValueFault.

        Parameters
        ----------
        stuck_val : float
            The constant value that replaces every entry in the faulted segment.
            This value may be positive, negative, integer, or floating-point.

        Notes
        -----
        The stuck value represents the sensor’s “frozen” output when it stops
        updating due to failure or stalled communication.
        """
        name = 'stuck value fault'
        super().__init__(name=name)
        super()._check_numeric_input(stuck_val, 'stuck_val')

        self.stuck_val = stuck_val


    def __call__(self, fault_length, list_output=False):
        r"""
        Generate a stuck-value sequence of the given length.

        Parameters
        ----------
        fault_length : int
            Length of the fault period. Every generated value will be equal to
            ``stuck_val``.

        list_output : bool, optional
            If ``True``, returns a Python list. Otherwise, updates internal
            fault state and returns a numpy array. Default is ``False``.

        Returns
        -------
        numpy.ndarray or list
            Array (or list) filled entirely with the constant stuck value.

        Notes
        -----
        This method does not require original signal values. It produces the
        stuck region directly, making it compatible with *both* preprocessing-
        based and injection-based workflows.
        """
        super()._check_fault_length(fault_length)
        fault_values = np.full(fault_length, self.stuck_val)

        if list_output:
            return super()._list_output(fault_values)
        super().update_fault(fault_values)
        return self.fault_values