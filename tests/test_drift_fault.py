import numpy as np
import pytest
from fault_injector.fault_lib.drift_fault import DriftFault


# Constructor & parameter tests
def test_default_params():
    f = DriftFault()
    assert f.drift_rate == 1


def test_custom_numeric_drift_rate():
    f = DriftFault(params={'drift_rate': 2})
    assert f.drift_rate == 2


@pytest.mark.parametrize("bad_value", [
    None,
    "string",
    [1, 2, 3],
    {"a": 1},
    object()
])
def test_invalid_drift_rate_raises(bad_value):
    with pytest.raises(ValueError, match="drift_rate"):
        DriftFault(params={'drift_rate': bad_value})


@pytest.mark.parametrize("valid_value", [
    1,
    2.5,
    -3,
    np.int32(5),
    np.int64(10),
    np.float32(1.5),
    np.float64(2.2)
])
def test_valid_numeric_drift_rate(valid_value):
    f = DriftFault(params={'drift_rate': valid_value})
    assert f.drift_rate == valid_value


# Data type validation tests
def test_non_array_input_raises():
    f = DriftFault()
    with pytest.raises(ValueError, match="must be an np.ndarray"):
        f([1, 2, 3])


def test_non_numeric_array_raises():
    f = DriftFault()
    x = np.array(["a", "b", "c"])
    with pytest.raises(ValueError, match="must contain numeric values"):
        f(x)


def test_numeric_array_passes():
    f = DriftFault()
    x = np.array([1, 2, 3])
    out = f(x)
    assert isinstance(out, np.ndarray)


# Drift behavior tests
def test_drift_default_rate():
    f = DriftFault()
    x = np.array([10, 10, 10])
    expected = x + np.array([1, 2, 3])
    np.testing.assert_array_equal(f(x), expected)


def test_drift_custom_rate():
    f = DriftFault(params={'drift_rate': 2})
    x = np.array([5, 5, 5, 5])
    drift = np.array([2, 4, 6, 8])
    expected = x + drift
    np.testing.assert_array_equal(f(x), expected)


def test_negative_drift_rate():
    # Negative step still produces a drift sequence
    f = DriftFault(params={'drift_rate': -1})
    x = np.array([1, 2, 3])
    drift = np.array([-1, -2, -3])
    expected = x + drift
    np.testing.assert_array_equal(f(x), expected)
