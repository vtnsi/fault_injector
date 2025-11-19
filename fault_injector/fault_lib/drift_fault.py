# -*- coding: utf-8 -*-
"""
drift fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault


class DriftFault(BaseFault):
    def __init__(self, drift_rate, continuous=False):
        r"""
        DriftFault
        ----------

        A fault class that applies a *linear drift* (increasing or decreasing trend)
        across a specified fault duration. The drift is defined by a constant
        ``drift_rate`` and may be generated either as independent segments or as one
        continuous, cumulative drift over multiple calls.

        This class inherits all state-handling, validation, and summary functionality
        from :class:`BaseFault` and :class:`FaultUtils`.

        .. rubric:: Purpose

        ``DriftFault`` simulates real-world sensor degradation, calibration drift,
        component aging, or gradual environmental shifts. Examples include:

        - Slowly drifting thermocouple readings
        - Long-term pressure bias changes
        - Voltage offsets from battery drain
        - ADC gain drift

        Drift faults are a core primitive used when testing anomaly detection,
        digital filtering robustness, and long-sequence fault tolerance.

        ---

        .. rubric:: Parameters

        **drift_rate** : *float*
            The constant rate of linear change per time step.
            Positive values produce upward drift; negative values produce downward drift.

        **continuous** : *bool, optional*
            Whether the drift *continues accumulating* across multiple calls:

            - ``False`` (default):
            Each call to :meth:`__call__` starts drift from zero.

            - ``True``:
            Drift continues from where the previous call ended.
            Useful for streaming or multi-segment applications.

        ---

        Drift Definition
        ----------------

        For a requested fault length :math:`N`, drift values are generated as:

        .. math::

            y_i = (i + s) \cdot r, \qquad i = 1, 2, \ldots, N

        where:

        - :math:`r` = ``drift_rate``
        - :math:`s` = ``prior`` offset
        (0 for the first call, or cumulative index when ``continuous=True``)

        When ``continuous=True``, the internal counter ``prior`` is incremented by
        the length of each generated segment, ensuring the next call picks up
        exactly where the previous one ended.

        ---

        Impact on Mean and Variance
        ----------------------------

        Consider a drift segment of length :math:`N`, beginning at index :math:`s`,
        with rate :math:`r`.

        The mean of the drift segment is:

        .. math::

            \bar{y}
            = \frac{1}{N} \sum_{i=1}^{N} (i + s) r
            = r \left( s + \frac{N + 1}{2} \right)

        If these drift values are *added* to an original signal :math:`x_i`, the new
        mean becomes:

        .. math::

            \bar{x + y}
            = \bar{x} + r \left( s + \frac{N + 1}{2} \right)

        ---

        The variance of a pure linear drift is:

        .. math::

            \mathrm{Var}(y)
            = r^2 \cdot \frac{N^2 - 1}{12}

        When drift is added to an existing signal, the variance increases by this
        quantity **plus** an interaction term if the underlying signal is not
        mean-centered.

        This analysis mirrors the behavior found in physical sensors where linear
        trends amplify variance over long durations.

        ---

        Behavior
        --------

        - Each call generates a new drift segment of specified length.
        - When ``continuous=False``:
        Each segment starts from zero drift.

        - When ``continuous=True``:
        Drift accumulates across calls, increasing the effective slope over time.

        - Supports list-output mode via ``list_output=True``.
        - Stores values internally via :meth:`update_fault` from :class:`FaultUtils`.

        ---

        Notes
        -----

        - ``DriftFault`` does **not** manipulate or reference original measured
        values; it simply generates the drift pattern. Injection happens elsewhere.
        - ``drift_rate`` must be numeric, and ``fault_length`` must be a positive integer.
        - ``reset()`` clears accumulated drift when using ``continuous=True``.

        """
        name = 'drift fault'
        super().__init__(name=name)
        super()._check_numeric_input(drift_rate, val_name='drift_rate')
        super()._check_bool_input(continuous, val_name='continuous')

        self.drift_rate = drift_rate
        self.prior = 0
        self.continuous = continuous


    def __call__(self, fault_length, list_output=False):
        """
        __call__(fault_length, list_output=False)
        -----------------------------------------

        Generate a linear drift sequence of length ``fault_length``.

        This method is the primary interface for producing drift values.
        It validates the requested length, constructs the drift array, updates
        internal state, and optionally returns the drift as a Python list.

        .. rubric:: Parameters

        **fault_length** : *int*
            Number of drift samples to generate.
            Must be a positive integer.

        **list_output** : *bool, optional*
            If ``True``, the drift values are:

            1. Converted to a Python ``list``
            2. Stored via :meth:`_list_output`
            3. Returned as a list

            Default is ``False`` (returns a numpy array).

        .. rubric:: Drift Behavior

        A linear drift sequence is generated as:

        .. math::

            y_i = (i + s) \cdot r, \qquad i = 1, 2, \ldots, N

        where:

        - :math:`N` = ``fault_length``
        - :math:`r` = ``drift_rate``
        - :math:`s` = ``prior`` (accumulated drift index when ``continuous=True``)

        When ``continuous=True``:
            - ``prior`` is incremented after each call
            - the next call resumes from the previous ending drift level

        When ``continuous=False``:
            - ``prior`` remains zero
            - each call starts from the same initial drift

        .. rubric:: Returns

        *numpy.ndarray* or *list*
            The generated drift values.

        Raises
        ------

        ``ValueError``
            If ``fault_length`` is not a positive integer.

        ---
        """
        super()._check_fault_length(fault_length)

        start = 1 + self.prior
        fault_values = np.arange(start, fault_length + start) * self.drift_rate

        if self.continuous:
            self.prior += fault_length
        if list_output:
            return super()._list_output(fault_values)

        super().update_fault(fault_values)
        return self.fault_values


    def reset(self):
        """
        reset()
        -------

        Reset the cumulative drift state.

        When ``continuous=True``, each call to :meth:`__call__` increases
        the internal index ``prior`` so that drift continues smoothly across
        multiple segments.

        Calling ``reset()`` restores:

        .. code-block:: python

            self.prior = 0

        This forces the next generated drift segment to behave exactly like
        the first call—starting from the initial drift value rather than
        continuing a previously accumulated trend.

        .. rubric:: Use Cases

        - Segmenting drift into independent batches
        - Restarting a simulation
        - Resetting between experiments or test loops

        ---
        """
        self.prior = 0