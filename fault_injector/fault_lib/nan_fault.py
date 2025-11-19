# -*- coding: utf-8 -*-
"""
nan fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault


class NaNFault(BaseFault):
    r"""
    NaN Fault
    =========
    A fault type that replaces all values within the fault interval with
    ``NaN`` (Not a Number). This simulates sensor dropout, missing data,
    or temporary loss of signal.

    The NaN fault produces an array of length ``fault_length`` where every
    entry is ``np.nan``.

    .. admonition:: Mathematical Definition

        For an original sequence :math:`x_i`, the NaN fault produces:

        .. math::

            y_i =
            \begin{cases}
            \text{NaN}, & 1 \le i \le N \\
            \end{cases}

        where:

        - :math:`N` = ``fault_length``
        - :math:`y_i` are the faulted values returned by :meth:`__call__`

        **Impact on Statistical Properties**

        Within the NaN-faulted region:

        - **Mean:** undefined
        - **Variance:** undefined
        - **Typical behavior in processing pipelines:**
          NaN values are omitted from statistical aggregations, effectively
          reducing the sample size and possibly biasing rolling-window
          algorithms.

        The NaN fault therefore models *complete information loss* in the
        faulted segment.

    Notes
    -----
    This fault type is widely used to represent:

    - sensor disconnects
    - bandwidth limitations or packet loss
    - data corruption
    - placeholder "unknown" values before interpolation or imputation

    """
    def __init__(self):
        """
        Initialize a NaN fault instance.

        The constructor simply registers the fault name and prepares the
        base class for managing fault updates. No configuration parameters
        are required because a NaN fault always produces a full-length
        array of ``np.nan`` values.

        Notes
        -----
        This fault begins unconfigured; the actual NaN sequence is created
        in :meth:`__call__`.
        """
        name = 'nan fault'
        super().__init__(name=name)


    def __call__(self, fault_length, list_output=False):
        r"""
        Generate a sequence of NaN values of the specified length.

        Parameters
        ----------
        fault_length : int
            Number of NaN entries to generate. Must be a positive integer.

        list_output : bool, optional
            If ``True``, return the faulted values as a Python list using
            :meth:`_list_output`.
            If ``False`` (default), return a NumPy array and store the fault
            internally for later inspection or plotting.

        Returns
        -------
        numpy.ndarray or list
            A sequence of ``NaN`` values of length ``fault_length``.

        Notes
        -----
        The generated sequence is:

        .. math::

            y = [\text{NaN}, \text{NaN}, \ldots, \text{NaN}]

        The method updates:

        - ``self.fault_values``
        - ``self.fault_length``

        following the BaseFault architecture.
        """
        super()._check_fault_length(fault_length)

        fault_values = np.full(fault_length, np.nan)
        if list_output:
            return super()._list_output(fault_values)

        super().update_fault(fault_values)
        self.fault_length = fault_length
        return self.fault_values