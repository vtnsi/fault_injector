import pytest
import numpy as np
from unittest.mock import patch
from fault_injector.fault_lib.stuck_value_fault import StuckValueFault


# -------------------------------------------------------------------------
# Constructor Tests
# -------------------------------------------------------------------------

def test_stuck_value_fault_init_sets_attributes():
    svf = StuckValueFault(stuck_val=5)
    assert svf.name == "stuck value fault"
    assert svf.stuck_val == 5


def test_stuck_value_fault_init_checks_numeric_input():
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_numeric_input") as chk:
        StuckValueFault(stuck_val=1.0)
        chk.assert_called_once_with(1.0, 'stuck_val')


# -------------------------------------------------------------------------
# Call Tests
# -------------------------------------------------------------------------

def test_call_generates_correct_ndarray():
    svf = StuckValueFault(stuck_val=7)
    length = 4
    captured = []

    def mock_update(arr):
        captured.append(arr)
        svf.fault_values = arr
        return arr

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=mock_update):
        result = svf(length)
        expected = np.full(length, 7)
        np.testing.assert_array_equal(captured[0], expected)
        assert np.array_equal(result, expected)


def test_call_generates_correct_list_output():
    svf = StuckValueFault(stuck_val=3)
    length = 5

    with patch("fault_injector.fault_lib.base_fault.BaseFault._list_output") as lo:
        lo.return_value = [3, 3, 3, 3, 3]
        result = svf(length, list_output=True)
        lo.assert_called_once()
        assert result == [3, 3, 3, 3, 3]


# -------------------------------------------------------------------------
# Edge Case Tests
# -------------------------------------------------------------------------

def test_call_length_one():
    svf = StuckValueFault(stuck_val=99)
    captured = []

    def mock_update(arr):
        captured.append(arr)
        svf.fault_values = arr
        return arr

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=mock_update):
        result = svf(1)
        expected = np.array([99])
        np.testing.assert_array_equal(captured[0], expected)
        assert np.array_equal(result, expected)


def test_call_length_zero_raises():
    svf = StuckValueFault(stuck_val=0)
    with pytest.raises(ValueError):
        svf(0)


def test_negative_stuck_val():
    svf = StuckValueFault(stuck_val=-10)
    captured = []

    def mock_update(arr):
        captured.append(arr)
        svf.fault_values = arr
        return arr

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=mock_update):
        result = svf(3)
        expected = np.full(3, -10)
        np.testing.assert_array_equal(captured[0], expected)
        assert np.array_equal(result, expected)


# -------------------------------------------------------------------------
# Type Validation Tests
# -------------------------------------------------------------------------

def test_call_checks_fault_length_called():
    svf = StuckValueFault(stuck_val=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length") as chk, \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault"):
        svf(4)
        chk.assert_called_once_with(4)
