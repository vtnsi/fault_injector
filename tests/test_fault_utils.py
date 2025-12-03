import numpy as np
import pytest
from fault_injector.fault_lib.utils import FaultUtils


class DummyFault(FaultUtils):
    """
    Minimal subclass to allow initialization and testing of FaultUtils methods.
    """
    def __init__(self):
        super().__init__()
        self.name = "dummy fault"


# --------------------------------------------------------------------------- #
# update_fault()
# --------------------------------------------------------------------------- #

def test_update_fault_basic():
    f = DummyFault()
    arr = [1, 2, 3]

    f.update_fault(arr)

    assert f.fault_values == arr
    assert f.fault_length == 3


def test_update_fault_invalid_type():
    f = DummyFault()

    with pytest.raises(ValueError):
        f.update_fault("bad")


def test_update_fault_invalid_length():
    f = DummyFault()

    with pytest.raises(ValueError):
        f.update_fault([])   # zero length → invalid


def test_update_fault_with_nan():
    f = DummyFault()
    arr = [1, np.nan, 3]

    # should not raise, but should print a warning
    f.update_fault(arr)

    assert np.isnan(f.fault_values[1])


# --------------------------------------------------------------------------- #
# create_zeros_array()
# --------------------------------------------------------------------------- #

def test_create_zeros_array_basic():
    f = DummyFault()
    z = f.create_zeros_array(5)

    assert isinstance(z, np.ndarray)
    assert len(z) == 5
    assert np.all(z == 0)


def test_create_zeros_array_invalid():
    f = DummyFault()

    with pytest.raises(ValueError):
        f.create_zeros_array(-1)

    with pytest.raises(ValueError):
        f.create_zeros_array(2.5)

    with pytest.raises(ValueError):
        f.create_zeros_array("bad")


# --------------------------------------------------------------------------- #
# _list_output()
# --------------------------------------------------------------------------- #

def test_list_output():
    f = DummyFault()
    out = f._list_output(np.array([1, 2, 3]))

    assert out == [1, 2, 3]              # must be list
    assert f.fault_values == [1, 2, 3]
    assert f.fault_length == 3


# --------------------------------------------------------------------------- #
# validation helpers
# --------------------------------------------------------------------------- #

def test_check_numeric_input_valid():
    f = DummyFault()
    f._check_numeric_input(10, "x")
    f._check_numeric_input(3.14, "x")
    f._check_numeric_input(np.int64(5), "x")


def test_check_numeric_input_invalid():
    f = DummyFault()

    with pytest.raises(ValueError):
        f._check_numeric_input("bad", "x")

    with pytest.raises(ValueError):
        f._check_numeric_input(None, "x")


def test_check_bool_input():
    f = DummyFault()

    f._check_bool_input(True, "flag")
    f._check_bool_input(False, "flag")

    with pytest.raises(ValueError):
        f._check_bool_input(1, "flag")

    with pytest.raises(ValueError):
        f._check_bool_input("true", "flag")


def test_check_list_array():
    f = DummyFault()

    f._check_list_array([1, 2, 3], "arr")
    f._check_list_array(np.array([1, 2]), "arr")

    with pytest.raises(ValueError):
        f._check_list_array("bad", "arr")


def test_check_fault_length_valid():
    f = DummyFault()
    f._check_fault_length(5)


def test_check_fault_length_invalid():
    f = DummyFault()

    with pytest.raises(ValueError):
        f._check_fault_length(0)

    with pytest.raises(ValueError):
        f._check_fault_length(-1)

    with pytest.raises(ValueError):
        f._check_fault_length(2.5)


def test_check_fault_values_invalid_type():
    f = DummyFault()

    with pytest.raises(ValueError):
        f._check_fault_values("bad")


def test_check_fault_values_invalid_length():
    f = DummyFault()

    with pytest.raises(ValueError):
        f._check_fault_values([])   # zero length invalid


def test_check_fault_values_nan_warning():
    f = DummyFault()
    arr = [1, np.nan]

    # should not raise
    f._check_fault_values(arr)
