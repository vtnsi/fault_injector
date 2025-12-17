import numpy as np
import pytest
from fault_injector.fault_lib.offset_fault import OffsetFault


# Constructor & parameter tests
def test_default_params():
    f = OffsetFault()
    assert f.offset_by == 1


def test_custom_numeric_offset_by():
    f = OffsetFault(params={'offset_by': 2})
    assert f.offset_by == 2


@pytest.mark.parametrize("bad_value", [
    None,
    "string",
    [1, 2, 3],
    {"a": 1},
    object()
])
def test_invalid_offset_by_raises(bad_value):
    with pytest.raises(ValueError, match="offset_by"):
        OffsetFault(params={'offset_by': bad_value})


@pytest.mark.parametrize("valid_value", [
    1,
    2.5,
    -3,
    np.int32(5),
    np.int64(10),
    np.float32(1.5),
    np.float64(2.2)
])
def test_valid_numeric_offset_by(valid_value):
    f = OffsetFault(params={'offset_by': valid_value})
    assert f.offset_by == valid_value


# Data type validation tests
def test_non_array_input_raises():
    f = OffsetFault()
    with pytest.raises(ValueError, match=r"Invalid 'x': must be array-like \(list, tuple, np\.ndarray\)"):
        f("test")


def test_non_numeric_array_raises():
    f = OffsetFault()
    x = np.array(["a", "b", "c"])
    with pytest.raises(ValueError, match="must contain numeric values"):
        f(x)


def test_numeric_array_passes():
    f = OffsetFault()
    x = np.array([1, 2, 3])
    out = f(x)
    assert isinstance(out, np.ndarray)


# offset behavior tests
def test_offset_default_rate():
    f = OffsetFault()
    x = np.array([10, 10, 10])
    expected = x + np.array([1, 1, 1])
    np.testing.assert_array_equal(f(x), expected)

def test_offset_list():
    f = OffsetFault()
    x = [10, 10, 10]
    expected = np.asarray(x) + np.array([1, 1, 1])
    np.testing.assert_array_equal(f(x), expected)

def test_offset_custom_rate():
    f = OffsetFault(params={'offset_by': 2})
    x = np.array([5, 5, 5, 5])
    offset = np.array([2, 2, 2, 2])
    expected = x + offset
    np.testing.assert_array_equal(f(x), expected)


def test_negative_offset_by():
    # Negative step still produces a offset sequence
    f = OffsetFault(params={'offset_by': -1})
    x = np.array([1, 2, 3])
    offset = np.array([-1, -1, -1])
    expected = x + offset
    np.testing.assert_array_equal(f(x), expected)
