import numpy as np
import pytest
from fault_injector.fault_lib.stuck_value_fault import StuckValueFault


# Constructor & parameter tests
def test_default_params():
    f = StuckValueFault()
    assert f.stuck_val == 1


def test_custom_numeric_stuck_val():
    f = StuckValueFault(params={'stuck_val': 2})
    assert f.stuck_val == 2


@pytest.mark.parametrize("bad_value", [
    None,
    "string",
    [1, 2, 3],
    {"a": 1},
    object()
])
def test_invalid_stuck_val_raises(bad_value):
    with pytest.raises(ValueError, match="stuck_val"):
        StuckValueFault(params={'stuck_val': bad_value})


@pytest.mark.parametrize("valid_value", [
    1,
    2.5,
    -3,
    np.int32(5),
    np.int64(10),
    np.float32(1.5),
    np.float64(2.2)
])
def test_valid_numeric_stuck_val(valid_value):
    f = StuckValueFault(params={'stuck_val': valid_value})
    assert f.stuck_val == valid_value


# Data type validation tests
def test_non_array_input_raises():
    f = StuckValueFault()
    with pytest.raises(ValueError, match="must be an np.ndarray"):
        f([1, 2, 3])


def test_non_numeric_array_raises():
    f = StuckValueFault()
    x = np.array(["a", "b", "c"])
    with pytest.raises(ValueError, match="must contain numeric values"):
        f(x)


def test_numeric_array_passes():
    f = StuckValueFault()
    x = np.array([1, 2, 3])
    out = f(x)
    assert isinstance(out, np.ndarray)


# stuck value behavior tests
def test_stuck_value_default_rate():
    f = StuckValueFault()
    x = np.array([10, 10, 10])
    expected = np.array([1, 1, 1])
    np.testing.assert_array_equal(f(x), expected)


def test_stuck_value_custom_rate():
    f = StuckValueFault(params={'stuck_val': 2})
    x = np.array([5, 5, 5, 5])
    expected = np.array([2, 2, 2, 2])
    np.testing.assert_array_equal(f(x), expected)


def test_negative_stuck_val():
    # Negative step still produces a stuck value sequence
    f = StuckValueFault(params={'stuck_val': -1})
    x = np.array([1, 2, 3])
    expected = np.array([-1, -1, -1])
    np.testing.assert_array_equal(f(x), expected)
