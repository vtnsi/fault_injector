import pytest
import numpy as np
from unittest.mock import patch
from fault_injector.fault_lib.base_fault import BaseFault
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------
# Constructor Tests
# -------------------------------------------------------------------------

def test_init_with_name_only():
    bf = BaseFault(name="custom")
    assert bf.name == "custom"
    assert bf.fault_values is None
    assert bf.fault_length is None

def test_init_with_default_name():
    bf = BaseFault()
    assert bf.name == "base fault"
    assert bf.fault_values is None
    assert bf.fault_length is None

def test_init_with_fault_values():
    vals = np.array([1, 2, 3])
    bf = BaseFault(fault_values=vals)
    # BaseFault should store the fault_values and length correctly
    assert np.array_equal(bf.fault_values, vals)
    assert bf.fault_length == 3

def test_init_with_fault_length():
    bf = BaseFault(fault_length=5)
    assert bf.fault_length == 5
    assert isinstance(bf.fault_values, np.ndarray)
    assert np.all(bf.fault_values == 0)

def test_init_none_args():
    bf = BaseFault()
    assert bf.fault_values is None
    assert bf.fault_length is None

# -------------------------------------------------------------------------
# __call__ Tests
# -------------------------------------------------------------------------

def test_call_with_array():
    bf = BaseFault()
    arr = np.array([5, 6, 7])
    result = bf(arr)
    assert np.array_equal(result, arr)
    assert np.array_equal(bf.fault_values, arr)
    assert bf.fault_length == 3

def test_call_with_list():
    bf = BaseFault()
    data = [1, 2, 3]
    result = bf(data)
    assert isinstance(result, list)
    assert result == data
    assert bf.fault_length == 3

def test_call_with_int_creates_zero_array():
    bf = BaseFault()
    length = 4
    result = bf(length)
    assert isinstance(result, np.ndarray)
    assert result.shape[0] == length
    assert np.all(result == 0)

def test_call_list_output_returns_list():
    bf = BaseFault()
    arr = np.array([1, 2, 3])
    result = bf(arr, list_output=True)
    assert isinstance(result, list)
    assert result == [1, 2, 3]

# -------------------------------------------------------------------------
# plot_fault Tests
# -------------------------------------------------------------------------

def test_plot_fault_runs(monkeypatch):
    bf = BaseFault()
    bf.fault_values = np.array([1, 2, 3])
    bf.fault_length = 3

    plotted = {"called": False}

    def fake_show():
        plotted["called"] = True

    monkeypatch.setattr(plt, "show", fake_show)

    # Should not raise
    bf.plot_fault(title="Test Plot", y_units="units")
    assert plotted["called"], "plt.show() should be called"

# -------------------------------------------------------------------------
# State consistency
# -------------------------------------------------------------------------

def test_fault_state_after_call():
    bf = BaseFault()
    arr = np.array([9, 8, 7, 6])
    bf(arr)
    assert bf.fault_length == len(arr)
    assert np.array_equal(bf.fault_values, arr)
