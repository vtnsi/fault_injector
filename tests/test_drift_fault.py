import pytest
import numpy as np
from unittest.mock import patch
from fault_injector.fault_lib.drift_fault import DriftFault

# -------------------------------------------------------------------------
# Constructor Tests
# -------------------------------------------------------------------------

def test_init_valid_inputs():
    df = DriftFault(drift_rate=0.5, continuous=True)
    assert df.drift_rate == 0.5
    assert df.continuous is True
    assert df.prior == 0
    assert df.name == "drift fault"

def test_init_checks_numeric_and_bool():
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_numeric_input") as cn, \
         patch("fault_injector.fault_lib.base_fault.BaseFault._check_bool_input") as cb:
        DriftFault(drift_rate=2.0, continuous=False)
        cn.assert_called_once()
        cb.assert_called_once()

# -------------------------------------------------------------------------
# Non-continuous Drift Tests
# -------------------------------------------------------------------------

def test_call_non_continuous_generates_correct_values():
    df = DriftFault(drift_rate=2.0, continuous=False)
    captured = []

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=lambda x: captured.append(x)), \
         patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"):

        df(4)
        expected = np.array([2, 4, 6, 8])  # start=1, multiply by drift_rate=2
        np.testing.assert_array_equal(captured[0], expected)

def test_call_non_continuous_prior_stays_zero():
    df = DriftFault(1.0, continuous=False)
    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"):

        df(3)
        assert df.prior == 0

# -------------------------------------------------------------------------
# Continuous Drift Tests
# -------------------------------------------------------------------------

def test_call_continuous_accumulates_prior():
    df = DriftFault(drift_rate=1.0, continuous=True)
    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"):

        df(3)
        assert df.prior == 3
        df(2)
        assert df.prior == 5

def test_call_continuous_correct_values_across_segments():
    df = DriftFault(drift_rate=1.0, continuous=True)
    captured = []

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=lambda x: captured.append(x)), \
         patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"):

        df(3)
        np.testing.assert_array_equal(captured[0], np.array([1, 2, 3]))

        df(2)
        np.testing.assert_array_equal(captured[1], np.array([4, 5]))

# -------------------------------------------------------------------------
# List Output Tests
# -------------------------------------------------------------------------

def test_call_list_output():
    df = DriftFault(drift_rate=1.0, continuous=False)

    with patch("fault_injector.fault_lib.base_fault.BaseFault._list_output") as lo, \
         patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"):

        lo.return_value = [10, 20, 30]
        result = df(3, list_output=True)
        lo.assert_called_once()
        assert result == [10, 20, 30]

def test_call_list_output_skips_update_fault():
    df = DriftFault(drift_rate=1.0, continuous=False)

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault") as uf, \
         patch("fault_injector.fault_lib.base_fault.BaseFault._list_output") as lo, \
         patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"):

        lo.return_value = [10, 20, 30]
        df(3, list_output=True)
        uf.assert_not_called()
        lo.assert_called_once()

# -------------------------------------------------------------------------
# Reset Tests
# -------------------------------------------------------------------------

def test_reset_sets_prior_to_zero():
    df = DriftFault(drift_rate=1.0, continuous=True)
    df.prior = 10
    df.reset()
    assert df.prior == 0

def test_reset_affects_next_call_continuous():
    df = DriftFault(drift_rate=1.0, continuous=True)
    captured = []

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=lambda x: captured.append(x)), \
         patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"):

        df(3)
        df.reset()
        df(2)

        np.testing.assert_array_equal(captured[0], np.array([1, 2, 3]))
        np.testing.assert_array_equal(captured[1], np.array([1, 2]))

# -------------------------------------------------------------------------
# Numeric Accuracy Tests
# -------------------------------------------------------------------------

def test_exact_numeric_drift_rate_scaling():
    df = DriftFault(drift_rate=0.25, continuous=False)
    captured = []

    with patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=lambda x: captured.append(x)), \
         patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"):

        df(4)
        expected = np.array([0.25, 0.5, 0.75, 1.0])
        np.testing.assert_array_almost_equal(captured[0], expected)
