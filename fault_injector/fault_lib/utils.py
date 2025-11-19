# -*- coding: utf-8 -*-
"""
utils for fault classes
"""
import numpy as np
import pandas as pd
import numbers


class FaultUtils:
    """
    FaultUtils
    ----------

    A utility mixin providing common validation, array creation, and summary
    functions shared across all fault classes.

    This class is not intended to be used directly. Instead, it supplies core
    functionality to :class:`BaseFault` and all fault subclasses such as
    :class:`DriftFault`, :class:`OffsetFault`, etc.

    It maintains the internal fault state (``fault_values`` and ``fault_length``),
    performs strict input validation, generates simple arrays, and provides a
    formatted statistical summary of the current fault.

    .. rubric:: Purpose

    ``FaultUtils`` acts as the underlying toolbox for the entire fault framework:

    - Validates numeric, boolean, and array-like inputs
    - Manages the storage of fault values
    - Provides standardized summary/diagnostic printing
    - Creates simple generated arrays (e.g., zero arrays)
    - Offers controlled list-output behavior used by ``BaseFault`` and subclasses

    This keeps the higher-level fault classes clean, readable, and focused solely
    on generating specific patterns of faulty behavior.

    ---

    .. rubric:: Attributes

    **fault_values** : *list or numpy.ndarray*
        The most recently updated fault data.

    **fault_length** : *int*
        Length of ``fault_values``. Always a positive integer.

    **name** : *str*
        A string identifier for the fault (required and provided by subclasses).

    ---

    .. rubric:: Methods Overview

    - :meth:`update_fault` — Validates and stores a new sequence of values
    - :meth:`create_zeros_array` — Generates a zero-filled array of requested length
    - :meth:`fault_summary` — Prints descriptive statistics of the current fault
    - Internal validation methods enforcing type and format constraints
    - :meth:`_list_output` — Converts input to list and updates internal state
    (used when a fault is requested in “list output mode”)

    ---


    Notes
    -----

    - ``FaultUtils`` is designed purely as a support class and does not generate
    faults on its own.
    - All higher-level faults rely on the validation guarantees provided here,
    ensuring consistent behavior across the entire library.
    """
    def __init__(self):
        self.fault_values = None
        self.fault_length = None
        self.name = None

    def update_fault(self, fault_values, summary=False):
        r"""
        update_fault(fault_values, summary=False)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Validate and store a new fault value sequence.

        .. rubric:: Parameters

        **fault_values** : *list or numpy.ndarray*
            Sequence of numeric values representing the fault.

        **summary** : *bool, optional*
            Whether to print a statistical summary immediately after updating
            (default: ``False``).

        .. rubric:: Behavior

        - Validates the sequence type and length
        - Stores ``fault_values`` and ``fault_length``
        - Warns if ``NaN`` values are present
        - Prints a confirmation message
        - Optionally prints the full summary block

        Raises
        ------

        ``ValueError``
            If the supplied values are not list- or array-like, or have non-positive length.

        ---
        """
        self._check_fault_values(fault_values)
        self.fault_values = fault_values
        self.fault_length = len(fault_values)

        print(f"Fault Updated!")
        if summary:
            self.fault_summary()

    def create_zeros_array(self, x):
        r"""
        create_zeros_array(x)
        ~~~~~~~~~~~~~~~~~~~~~

        Generate a zero-filled numpy array of length ``x``.

        .. rubric:: Parameters

        **x** : *int*
            Length of the array to create. Must be a positive integer.

        .. rubric:: Returns

        *numpy.ndarray*
            A zero-initialized array of size ``x``.

        Raises
        ------

        ``ValueError``
            If ``x`` is not a positive integer.

        ---
        """
        self._check_fault_length(x, val_name='x')
        x = np.zeros(x)
        print(f"Created array of {len(x)} values")
        return x

    def fault_summary(self):
        r"""
        fault_summary()
        ~~~~~~~~~~~~~~~

        Print a detailed, formatted summary of the current fault values.

        The summary includes:

        - A header containing the fault name
        - A statistical table (via :mod:`pandas.DataFrame.describe`)
        - First/last 10 values when available
        - Full values when fewer than 10 are present

        .. rubric:: Notes

        The method assumes that:

        - ``fault_values`` has already been set
        - ``self.name`` has been defined by the subclass (e.g., ``"drift fault"``)

        Raises
        ------

        ``ValueError``
            If ``fault_length`` is invalid or missing.

        ---
        """
        self._check_fault_length(self.fault_length)
        print(f'\n ~~~~~  {self.name} ~~~~~ \n')
        print(f'Glimpse of fault_values \n')
        print(pd.DataFrame(np.array(self.fault_values), columns=['statistics']).describe())

        if self.fault_length > 10:
            print(f"\n First 10 values the fault: \n {self.fault_values[:10]}")
            print(f"\n Last 10 values the fault: \n {self.fault_values[-10:]}")
        else:
            print(f"\n Fault values: \n {self.fault_values}")


    # internal methods
    def _list_output(self, fault_values):
        """
        _list_output(fault_values)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        Internal helper for “list output” mode.

        Used by :class:`BaseFault` and specific fault classes to:

        1. Convert the given values to a Python list
        2. Update internal fault state
        3. Return the list representation

        This ensures consistency across fault types when returning list formats.

        .. rubric:: Returns

        *list*
            The updated fault values as a list.

        ---
        """
        fault_values = list(fault_values)
        self.update_fault(fault_values)
        return self.fault_values


    # checks
    def _check_numeric_input(self, val, val_name):
        """
        _check_numeric_input(val, val_name)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Ensures that ``val`` is a numeric type.

        Accepts Python numeric types and numpy scalar types
        (``np.int64``, ``np.float64``, etc.).

        Raises
        ------

        ``ValueError``
            If ``val`` is not numeric.

        ---
        """
        if not isinstance(val, numbers.Number):
            raise ValueError(f"Invalid Input ({val_name}): \n must be numbers (float, int, np.int64, np.float32, np.float64, np.int32, etc.).")

    def _check_bool_input(self, val, val_name):
        """
        _check_bool_input(val, val_name)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Validates that ``val`` is a boolean.

        Raises
        ------

        ``ValueError``
            If ``val`` is not exactly ``True`` or ``False``.

        ---
        """
        if not isinstance(val, bool):
            raise ValueError(f"Invalid Input ({val_name}): \n must be a bool value (True or False).")

    def _check_list_array(self, val, val_name):
        """
        _check_list_array(val, val_name)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Ensures that ``val`` is a list or numpy array.

        Raises
        ------

        ``ValueError``
            If the type is not list- or array-like.

        ---
        """
        if not isinstance(val, (np.ndarray, list)):
            raise ValueError(f"Invalid Input ({val_name}): \n must be a list or array.")

    def _check_fault_length(self, val, val_name='fault_length'):
        """
        _check_fault_length(val, val_name='fault_length')
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Validates that ``val`` is a positive integer.

        Raises
        ------

        ``ValueError``
            If the value is not a positive integer.

        ---
        """
        if not isinstance(val, int):
            raise ValueError(f"Invalid Input ({val_name}): \n must be a positive int.")
        elif not val > 0:
            raise ValueError(f"Invalid Input ({val_name}): \n must be a positive int.")

    def _check_fault_values(self, fault_values):
        """
        _check_fault_values(fault_values)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Validates an entire sequence of fault values:

        - Must be list- or array-like
        - Must have positive length
        - Issues a warning if any ``NaN`` values are present

        ---
        """
        self._check_list_array(fault_values, 'fault_values')
        self._check_fault_length(len(fault_values), val_name="length of fault_values")
        if np.isnan(np.array(fault_values)).any():
            print("Warning: fault_values contains nan values")
