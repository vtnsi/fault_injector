import numpy as np
import pytest
from fault_injector.fault_lib.uniform_noise_fault import UniformNoiseFault


# Constructor & parameter tests
def test_default_params():
    f = UniformNoiseFault()
    assert f.min_val == 0
    assert f.max_val == 1


def test_custom_numeric_min_val_and_max_val():
    f = UniformNoiseFault(params={'min_val': 2, 'max_val':5})
    assert f.min_val == 2
    assert f.max_val == 5


@pytest.mark.parametrize("bad_value", [
    None,
    "string",
    [1, 2, 3],
    {"a": 1},
    object()
])
def test_invalid_min_val_raises(bad_value):
    with pytest.raises(ValueError, match='min_val'):
        UniformNoiseFault(params={'min_val': bad_value, 'max_val':1})


@pytest.mark.parametrize("bad_value", [
    None,
    "string",
    [1, 2, 3],
    {"a": 1},
    object(),
    -1
])
def test_invalid_max_val_raises(bad_value):
    with pytest.raises(ValueError, match="max_val"):
        UniformNoiseFault(params={'min_val':0, 'max_val':bad_value})



@pytest.mark.parametrize("valid_value", [
    1,
    2.5,
    -3,
    np.int32(5),
    np.int64(10),
    np.float32(1.5),
    np.float64(2.2)
])
def test_valid_numeric_min_val(valid_value):
    f = UniformNoiseFault(params={'min_val': valid_value, 'max_val':100})
    assert f.min_val == valid_value

@pytest.mark.parametrize("valid_value", [
    1,
    2.5,
    np.int32(5),
    np.int64(10),
    np.float32(1.5),
    np.float64(2.2)
])
def test_valid_positive_max_val(valid_value):
    f = UniformNoiseFault(params={'min_val': 0, 'max_val':valid_value})
    assert f.max_val == valid_value

# Data type validation tests
def test_non_array_input_raises():
    f = UniformNoiseFault()
    with pytest.raises(ValueError, match=r"Invalid 'x': must be array-like \(list, tuple, np\.ndarray\)"):
        f("test")


def test_non_numeric_array_raises():
    f = UniformNoiseFault()
    x = np.array(["a", "b", "c"])
    with pytest.raises(ValueError, match="must contain numeric values"):
        f(x)


def test_numeric_array_passes():
    f = UniformNoiseFault()
    x = np.array([1, 2, 3])
    out = f(x)
    assert isinstance(out, np.ndarray)

def test_numeric_list_passes():
    f = UniformNoiseFault()
    x = [1, 2, 3]
    out = f(x)
    assert isinstance(out, np.ndarray)