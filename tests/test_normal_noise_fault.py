import numpy as np
import pytest
from fault_injector.fault_lib.normal_noise_fault import NormalNoiseFault


# Constructor & parameter tests
def test_default_params():
    f = NormalNoiseFault()
    assert f.mu == 0
    assert f.sigma == 1


def test_custom_numeric_mu_and_sigma():
    f = NormalNoiseFault(params={'mu': 2, 'sigma':5})
    assert f.mu == 2
    assert f.sigma == 5


@pytest.mark.parametrize("bad_value", [
    None,
    "string",
    [1, 2, 3],
    {"a": 1},
    object()
])
def test_invalid_mu_raises(bad_value):
    with pytest.raises(ValueError, match="mu"):
        NormalNoiseFault(params={'mu': bad_value, 'sigma':1})


@pytest.mark.parametrize("bad_value", [
    None,
    "string",
    [1, 2, 3],
    {"a": 1},
    object(),
    -1
])
def test_invalid_sigma_raises(bad_value):
    with pytest.raises(ValueError, match="sigma"):
        NormalNoiseFault(params={'mu':0, 'sigma':bad_value})



@pytest.mark.parametrize("valid_value", [
    1,
    2.5,
    -3,
    np.int32(5),
    np.int64(10),
    np.float32(1.5),
    np.float64(2.2)
])
def test_valid_numeric_mu(valid_value):
    f = NormalNoiseFault(params={'mu': valid_value, 'sigma':1})
    assert f.mu == valid_value

@pytest.mark.parametrize("valid_value", [
    1,
    2.5,
    np.int32(5),
    np.int64(10),
    np.float32(1.5),
    np.float64(2.2)
])
def test_valid_positive_sigma(valid_value):
    f = NormalNoiseFault(params={'mu': 0, 'sigma':valid_value})
    assert f.sigma == valid_value

# Data type validation tests
def test_non_array_input_raises():
    f = NormalNoiseFault()
    with pytest.raises(ValueError, match=r"Invalid 'x': must be array-like \(list, tuple, np\.ndarray\)"):
        f("test")


def test_non_numeric_array_raises():
    f = NormalNoiseFault()
    x = np.array(["a", "b", "c"])
    with pytest.raises(ValueError, match="must contain numeric values"):
        f(x)


def test_numeric_array_passes():
    f = NormalNoiseFault()
    x = np.array([1, 2, 3])
    out = f(x)
    assert isinstance(out, np.ndarray)

