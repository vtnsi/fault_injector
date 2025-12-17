import numpy as np
import pytest
from fault_injector.fault_lib.nan_fault import NaNFault


# Constructor & parameter tests
def test_init():
    f = NaNFault()
    assert f.name == 'nan_fault'


# Data type validation tests
def test_non_array_input_raises():
    f = NaNFault()
    with pytest.raises(ValueError, match=r"Invalid 'x': must be array-like \(list, tuple, np\.ndarray\)"):
        f({'key':1})


def test_non_numeric_array_raises():
    f = NaNFault()
    x = np.array(["a", "b", "c"])
    with pytest.raises(ValueError, match="must contain numeric values"):
        f(x)


# nan behavior tests
def test_nan_output():
    f = NaNFault()
    x = np.array([10, 10, 10])
    expected = np.array([np.nan, np.nan, np.nan])
    np.testing.assert_array_equal(f(x), expected)


def test_nan_list_value():
    f = NaNFault()
    x = [5, 5, 5, 5]
    expected = np.array([np.nan, np.nan, np.nan, np.nan])
    np.testing.assert_array_equal(f(x), expected)