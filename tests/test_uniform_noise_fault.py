import pytest
import numpy as np
from unittest.mock import patch
from fault_injector.fault_lib.uniform_noise_fault import UniformNoiseFault


# -------------------------------------------------------------------------
# Constructor Tests
# -------------------------------------------------------------------------

def test_uniform_noise_fault_init_sets_attributes():
    unf = UniformNoiseFault(min_val=-1.0, max_val=1.0)
    assert unf.name == "uniform noise fault"
    assert unf.min_val == -1.0
    assert unf.max_val == 1.0


def test_uniform_noise_fault_init_checks_numeric_input():
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_numeric_input") as chk:
        UniformNoiseFault(min_val=0.0, max_val=1.0)
        assert chk.call_count == 2
        chk.assert_any_call(0.0, 'min_val')
        chk.assert_any_call(1.0, 'max_val')


# -------------------------------------------------------------------------
# Call Tests
# -------------------------------------------------------------------------

def test_call_generates_correct_ndarray():
    np.random.seed(0)
    unf = UniformNoiseFault(min_val=0, max_val=1)
    length = 5
    captured = []

    def mock_update(arr):
        captured.append(arr)
        unf.fault_values = arr
        return arr

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=mock_update):
        result = unf(length)
        assert isinstance(result, np.ndarray)
        assert len(result) == length
        assert np.all(result >= 0) and np.all(result <= 1)
        np.testing.assert_array_equal(result, captured[0])


def test_call_generates_correct_list_output():
    np.random.seed(0)
    unf = UniformNoiseFault(min_val=0, max_val=1)
    length = 3
    with patch("fault_injector.fault_lib.base_fault.BaseFault._list_output") as lo:
        lo.return_value = [0.1, 0.2, 0.3]
        result = unf(length, list_output=True)
        lo.assert_called_once()
        assert result == [0.1, 0.2, 0.3]


# -------------------------------------------------------------------------
# Edge Case Tests
# -------------------------------------------------------------------------

def test_call_length_one():
    np.random.seed(0)
    unf = UniformNoiseFault(min_val=0, max_val=2)
    captured = []

    def mock_update(arr):
        captured.append(arr)
        unf.fault_values = arr
        return arr

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=mock_update):
        result = unf(1)
        assert result.shape == (1,)
        np.testing.assert_array_equal(result, captured[0])


def test_call_length_zero_raises():
    unf = UniformNoiseFault(min_val=0, max_val=1)
    with pytest.raises(ValueError):
        unf(0)


def test_min_equals_max():
    unf = UniformNoiseFault(min_val=5, max_val=5)
    result = unf(3)
    expected = np.array([5, 5, 5])
    np.testing.assert_array_equal(result, expected)


# -------------------------------------------------------------------------
# Type Validation Tests
# -------------------------------------------------------------------------

def test_call_checks_fault_length_called():
    unf = UniformNoiseFault(min_val=0, max_val=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length") as chk, \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault"):
        unf(4)
        chk.assert_called_once_with(4)
