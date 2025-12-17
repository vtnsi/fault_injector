import numpy as np
import pytest
from fault_injector.fault_lib.base_fault import BaseFault


# Constructor tests
def test_default_constructor():
    f = BaseFault()
    assert f.name == "base_fault"


# __call__ behavior tests
def test_call_returns_input_unchanged():
    f = BaseFault()
    x = np.array([1, 2, 3])
    out = f(x)
    np.testing.assert_array_equal(out, x)


def test_call_with_list():
    f = BaseFault()
    x = [1, 2, 3]
    out = f(x)
    assert out == x


# _check_data_type tests
@pytest.mark.parametrize("bad_value", [
    None,
    5,
    "string",
    {"a": 1},
    object()
])
def test_check_data_type_non_array_like_raises(bad_value):
    f = BaseFault()
    with pytest.raises(ValueError, match="array-like"):
        f._check_data_type(bad_value)


def test_check_data_type_non_numeric_array_raises():
    f = BaseFault()
    x = ["a", "b", "c"]
    with pytest.raises(ValueError, match="numeric values"):
        f._check_data_type(x)


@pytest.mark.parametrize("valid_value", [
    [1, 2, 3],
    (1.0, 2.0, 3.0),
    np.array([1, 2, 3]),
    np.array([1.5, 2.5, 3.5]),
    np.array([1, 2, 3], dtype=np.int32),
    np.array([1, 2, 3], dtype=np.float64),
])
def test_check_data_type_numeric_array_passes(valid_value):
    f = BaseFault()
    out = f._check_data_type(valid_value)
    assert isinstance(out, np.ndarray)


def test_check_data_type_returns_numpy_array():
    f = BaseFault()
    x = [1, 2, 3]
    out = f._check_data_type(x)
    assert isinstance(out, np.ndarray)
    np.testing.assert_array_equal(out, np.array(x))
