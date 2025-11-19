import pytest
import numpy as np
from unittest.mock import patch

from fault_injector.fault_lib.offset_fault import OffsetFault


# -------------------------------------------------------------------------
# Constructor Tests
# -------------------------------------------------------------------------

def test_offset_fault_init_sets_attributes():
    of = OffsetFault(offset_by=2.5)
    assert of.name == "offset fault"
    assert of.offset_by == 2.5


def test_offset_fault_init_checks_numeric_input():
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_numeric_input") as chk:
        OffsetFault(offset_by=1.0)
        chk.assert_called_once_with(1.0, 'offset_by')


# -------------------------------------------------------------------------
# Call Tests
# -------------------------------------------------------------------------

def test_call_applies_offset_to_ndarray():
    arr = np.array([1.0, 2.0, 3.0])
    of = OffsetFault(offset_by=2.0)
    captured = []

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=lambda arr: captured.append(arr)):
        result = of(arr)
        expected = arr + 2.0
        np.testing.assert_array_equal(captured[0], expected)
        # BaseFault __call__ returns the updated fault_values
        assert np.array_equal(result, expected)


def test_call_applies_offset_to_ndarray():
    arr = np.array([1.0, 2.0, 3.0])
    of = OffsetFault(offset_by=2.0)
    captured = []

    def mock_update_fault(arr_in):
        captured.append(arr_in)
        of.fault_values = arr_in
        return arr_in

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=mock_update_fault):
        result = of(arr)
        expected = arr + 2.0
        np.testing.assert_array_equal(captured[0], expected)
        # __call__ now returns proper array
        assert np.array_equal(result, expected)


def test_call_integer_input_creates_zeros_and_offsets():
    of = OffsetFault(offset_by=5)
    captured = []

    def mock_update_fault(arr_in):
        captured.append(arr_in)
        of.fault_values = arr_in
        return arr_in

    with patch("fault_injector.fault_lib.base_fault.BaseFault.create_zeros_array") as cz, \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=mock_update_fault):
        cz.return_value = np.zeros(3)
        result = of(3)
        expected = np.zeros(3) + 5
        cz.assert_called_once_with(3)
        np.testing.assert_array_equal(captured[0], expected)
        assert np.array_equal(result, expected)



def test_call_integer_input_list_output():
    of = OffsetFault(offset_by=10)
    with patch("fault_injector.fault_lib.base_fault.BaseFault.create_zeros_array") as cz, \
         patch("fault_injector.fault_lib.base_fault.BaseFault._list_output") as lo:
        cz.return_value = np.zeros(2)
        lo.return_value = [10, 10]
        result = of(2, list_output=True)
        lo.assert_called_once()
        assert result == [10, 10]


# -------------------------------------------------------------------------
# Edge Case Tests
# -------------------------------------------------------------------------

def test_empty_list_input_returns_list():
    of = OffsetFault(offset_by=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._list_output") as lo:
        lo.return_value = []
        result = of([])
        lo.assert_called_once()
        assert result == []


def test_negative_numbers_in_list_input():
    lst = [-1, -2, -3]
    of = OffsetFault(offset_by=2)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._list_output") as lo:
        lo.return_value = [1, 0, -1]
        result = of(lst)
        lo.assert_called_once()
        assert result == [1, 0, -1]


# -------------------------------------------------------------------------
# Type Validation Tests
# -------------------------------------------------------------------------

def test_call_checks_list_array_called_on_ndarray():
    arr = np.array([1, 2, 3])
    of = OffsetFault(offset_by=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_list_array") as chk, \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault"):
        of(arr)
        chk.assert_called_once_with(arr, 'x')
