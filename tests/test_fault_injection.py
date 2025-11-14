import numpy as np
import pytest
from fault_injector.injector import FaultInjection


# Basic Constructor Tests
def test_init_basic():
    fi = FaultInjection([1, 2, 3, 4])
    assert fi.values == [1, 2, 3, 4]
    assert fi.original_values == [1, 2, 3, 4]
    assert fi.start == 0
    assert fi.stop == 4
    assert fi.fault_direction == -1  # default decreasing


def test_init_invalid_values():
    with pytest.raises(Exception):
        FaultInjection([])

    with pytest.raises(Exception):
        FaultInjection(["bad"])


def test_init_start_stop_bounds():
    fi = FaultInjection([1, 2, 3, 4], start=1, stop=3)
    assert fi.start == 1
    assert fi.stop == 3


# restore_values()
def test_restore_values():
    fi = FaultInjection([10, 20, 30])
    fi.values = [99, 99, 99]
    fi.restore_values()
    assert fi.values == [10, 20, 30]


# Drift Fault
def test_inject_drift_fixed_rate():
    values = [10, 10, 10, 10, 10]
    fi = FaultInjection(values, start=1, stop=4, increasing=1)

    fi.inject_drift(drift_rate=1.0)

    assert fi.values == [10, 11, 12, 13, 10]


# Offset Fault
def test_inject_offset_fixed():
    values = [10, 20, 30, 40]
    fi = FaultInjection(values, start=1, stop=3, increasing=1)

    fi.inject_offset(0.1)  # offset = 2.5

    assert fi.values == [10, 22.5, 32.5, 40]


# NaN Fault
def test_inject_nan():
    fi = FaultInjection([1, 2, 3, 4], start=1, stop=3)
    fi.inject_nan()

    assert fi.values[0] == 1
    assert np.isnan(fi.values[1])
    assert np.isnan(fi.values[2])
    assert fi.values[3] == 4


# Stuck Value Fault
def test_inject_stuck_value_fixed():
    fi = FaultInjection([5, 5, 5, 5], start=2, stop=4)
    fi.inject_stuck_value(stuck_val=99)

    assert fi.values == [5, 5, 99, 99]


# Noise Injection
def test_inject_gaussian_noise():
    np.random.seed(0)
    fi = FaultInjection([1, 1, 1, 1], start=0, stop=4)
    fi.inject_noise("gaussian", params=[0, 1])

    assert not np.allclose(fi.values, [1, 1, 1, 1])


def test_inject_uniform_noise():
    np.random.seed(0)
    fi = FaultInjection([1, 1, 1, 1], start=0, stop=4)
    fi.inject_noise("uniform", params=[-1, 1])

    assert not np.allclose(fi.values, [1, 1, 1, 1])
