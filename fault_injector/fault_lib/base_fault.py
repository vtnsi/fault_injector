# -*- coding: utf-8 -*-
"""
base fault class
"""
import numpy as np
import matplotlib.pyplot as plt
from fault_injector.fault_lib.utils import FaultUtils as utils


class BaseFault(utils):
    """
    BaseFault
    ---------

    The foundational class for all fault types in the library.

    ``BaseFault`` provides common behavior for storing, validating, and updating
    fault values, while delegating numerical validation and summary operations
    to :class:`FaultUtils`. All higher-level fault generators (e.g.,
    :class:`DriftFault`, :class:`OffsetFault`, :class:`NoiseFault`, etc.)
    inherit from this class and override the :meth:`__call__` method to produce
    their specific fault patterns.

    ``BaseFault`` may also be used directly as a simple container for externally
    supplied fault sequences.

    .. rubric:: Purpose

    ``BaseFault`` standardizes core behaviors:

    - Initializes fault values from raw data or from a requested length
    - Validates all input sequences and dimensions
    - Provides a unified callable interface for updating faults
    - Implements optional list-output mode
    - Offers quick plotting utilities for debugging and visualization
    - Ensures consistent fault storage (``fault_values``, ``fault_length``)

    This base class ensures that all fault subclasses interact seamlessly with
    injection pipelines and maintain consistent behavior across the entire
    fault framework.

    ---

    .. rubric:: Parameters (Constructor)

    **name** : *str, optional*
        Name of the fault instance. Defaults to ``"base fault"`` when omitted.

    **fault_values** : *list or numpy.ndarray, optional*
        Sequence of values used to initialize the fault. When supplied:

        - Values are validated through :class:`FaultUtils`
        - ``fault_length`` is inferred
        - The internal state is initialized accordingly

    **fault_length** : *int, optional*
        Length of the fault when explicit values are **not** provided. In this
        case:

        - The length is validated
        - ``fault_values`` is initialized as a zero array of that length

    If neither argument is provided, the internal state remains uninitialized
    until :meth:`__call__` or :meth:`update_fault` is invoked.

    ---

    .. rubric:: Internal State

    **fault_values** : *list or numpy.ndarray*
        The current stored fault values.

    **fault_length** : *int*
        Length of ``fault_values``.

    **name** : *str*
        Human-readable label used in summaries and plots.

    ---

    Behavior
    --------

    Initialization
    ~~~~~~~~~~~~~~

    ``BaseFault`` supports two primary initialization pathways:

    1. **User supplies fault values**
       The values are validated and stored directly.

    2. **User supplies fault length only**
       A zero-filled array of that length is created.

    If neither is supplied, the object acts as an empty shell until updated.

    ---
    """
    def __init__(self, name=None, fault_values=None, fault_length=None):
        super().__init__()
        if name == None:
            name = 'base fault'

        self.name = name

        if fault_values is not None:
            super().update_fault(fault_values)
        elif fault_length != None:
            super()._check_fault_length(fault_length)
            self.fault_length = fault_length
            self.fault_values = super().create_zeros_array(fault_length)
        else:
            self.fault_values = fault_values
            self.fault_length = fault_length


    def __call__(self, x, list_output=False):
        r"""
        __call__(x, list_output=False)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Update the internal fault values.

        ``x`` may be:

        - A list or numpy array of numeric values
        - A positive integer, which is interpreted as a request to create a
          zero-filled array of length ``x``

        If ``list_output=True``, the method returns the resulting values as a
        Python list; otherwise it returns the internally stored sequence in its
        native format.

        .. rubric:: Parameters

        **x** : *list, numpy.ndarray, or int*
            The new fault data or the requested zero-array length.

        **list_output** : *bool, optional*
            Whether to return the updated values as a Python list. Defaults to
            ``False``.

        .. rubric:: Returns

        *list or numpy.ndarray*
            The updated fault values.

        Raises
        ------

        ``ValueError``
            If ``x`` is an invalid type (non-numeric, negative integer, etc.).

        ---
        """
        if not isinstance(x, (list, np.ndarray)):
            x = super().create_zeros_array(x)

        if list_output:
            return super()._list_output(x)
        super().update_fault(x)
        return self.fault_values


    def plot_fault(self, title=None, y_units=None):
        r"""
        plot_fault(title=None, y_units=None)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Produce a matplotlib line plot of the current fault values.

        This method is primarily intended for debugging, development, and
        exploratory data inspection.

        .. rubric:: Parameters

        **title** : *str, optional*
            Custom plot title. Defaults to ``"<name> plot"`` when omitted.

        **y_units** : *str, optional*
            Label for the y-axis. Defaults to ``"Units of Original Values"``.

        .. rubric:: Behavior

        - Validates that ``fault_values`` is properly set
        - Plots samples from index ``0`` to ``fault_length - 1``
        - Draws the fault using a red line
        - Includes a grid and axis labels for readability

        ---
        """
        super()._check_fault_values(self.fault_values)
        if title == None:
            title = f'{self.name} plot'

        if y_units == None:
            y_units = 'Units of Original Values'

        plt.plot(range(self.fault_length), self.fault_values, c='red')

        plt.xlim((-1, self.fault_length+1))
        plt.xlabel("Time During Fault")
        plt.ylabel(y_units)
        plt.title(title)
        plt.grid()
        plt.show()
