import numpy as np
import pytest
from fault_injector.injector import Injector

# Dummy fault classes for testing
class IdentityFault:
    """Returns input unchanged"""
    def __call__(self, x):
        return x


class AddOneFault:
    """Adds 1 to every element"""
    def __call__(self, x):
        return x + 1


class BadFaultClass:
    """Used to test passing a class instead of an instance"""
    def __call__(self, x):
        return x

# Constructor & parameter tests
def test_default_params():
    inj = Injector(fault=IdentityFault())
    assert inj.start == 0
    assert inj.stop == -1


def test_custom_params():
    inj = Injector(
        fault=IdentityFault(),
        params={"start": 1, "stop": 3}
    )
    assert inj.start == 1
    assert inj.stop == 3


def test_none_params_are_defaulted():
    inj = Injector(
        fault=IdentityFault(),
        params={"start": None, "stop": None}
    )
    assert inj.start == 0
    assert inj.stop == -1


@pytest.mark.parametrize("bad_value", [
    "string",
    1.5,
    {},
])
def test_invalid_start_type_raises(bad_value):
    with pytest.raises(ValueError, match="start"):
        Injector(
            fault=IdentityFault(),
            params={"start": bad_value, "stop": 1}
        )


@pytest.mark.parametrize("bad_value", [
    "string",
    1.5,
    {},
])
def test_invalid_stop_type_raises(bad_value):
    with pytest.raises(ValueError, match="stop"):
        Injector(
            fault=IdentityFault(),
            params={"start": 0, "stop": bad_value}
        )

# Data type validation tests
@pytest.mark.parametrize("bad_x", [
    None,
    5,
    "string",
    {"a": 1},
    object(),
])
def test_non_array_like_input_raises(bad_x):
    inj = Injector(fault=IdentityFault())
    with pytest.raises(ValueError, match="array-like"):
        inj.inject_fault(bad_x)


def test_non_numeric_array_raises():
    inj = Injector(fault=IdentityFault())
    x = ["a", "b", "c"]
    with pytest.raises(ValueError, match="numeric values"):
        inj.inject_fault(x)


@pytest.mark.parametrize("valid_x", [
    [1, 2, 3],
    (1.0, 2.0, 3.0),
    np.array([1, 2, 3]),
    np.array([1.5, 2.5, 3.5]),
    np.array([1, 2, 3], dtype=np.int32),
])
def test_numeric_array_like_passes(valid_x):
    inj = Injector(fault=IdentityFault())
    out = inj.inject_fault(valid_x)
    assert isinstance(out, np.ndarray)

# Index parameter range tests
def test_start_out_of_range_raises():
    inj = Injector(
        fault=IdentityFault(),
        params={"start": 10, "stop": 12}
    )
    x = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="start"):
        inj.inject_fault(x)


def test_stop_out_of_range_raises():
    inj = Injector(
        fault=IdentityFault(),
        params={"start": 0, "stop": 10}
    )
    x = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="stop"):
        inj.inject_fault(x)


def test_negative_start_out_of_range_raises():
    inj = Injector(
        fault=IdentityFault(),
        params={"start": -10, "stop": -1}
    )
    x = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="start"):
        inj.inject_fault(x)


def test_negative_stop_out_of_range_raises():
    inj = Injector(
        fault=IdentityFault(),
        params={"start": 0, "stop": -10}
    )
    x = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="stop"):
        inj.inject_fault(x)

# Fault injection behavior tests
def test_full_array_injection_default_params():
    inj = Injector(fault=AddOneFault())
    x = np.array([1, 2, 3])

    out = inj.inject_fault(x)

    np.testing.assert_array_equal(out, [2, 3, 3])


def test_partial_array_injection():
    inj = Injector(
        fault=AddOneFault(),
        params={"start": 1, "stop": 3}
    )
    x = np.array([10, 20, 30, 40])

    out = inj.inject_fault(x)

    expected = np.array([10, 21, 31, 40])
    np.testing.assert_array_equal(out, expected)


def test_negative_stop_index():
    inj = Injector(
        fault=AddOneFault(),
        params={"start": 0, "stop": -1}
    )
    x = np.array([1, 2, 3, 4])

    out = inj.inject_fault(x)

    expected = np.array([2, 3, 4, 4])
    np.testing.assert_array_equal(out, expected)


def test_original_input_not_modified():
    inj = Injector(fault=AddOneFault())
    x = np.array([1, 2, 3])

    _ = inj.inject_fault(x)

    np.testing.assert_array_equal(x, [1, 2, 3])

# Fault instance validation
def test_fault_class_is_accepted_by_default():
    inj = Injector(fault=BadFaultClass)
    x = np.array([1, 2, 3])

    with pytest.raises(TypeError):
        inj.inject_fault(x)
