import pytest
import numpy as np
from unittest.mock import patch
from fault_injector.fault_lib.normal_noise_fault import NormalNoiseFault

# -------------------------------------------------------------------------
# Constructor Tests
# -------------------------------------------------------------------------

def test_normal_noise_fault_init_sets_attributes():
    nf = NormalNoiseFault(mu=0.5, sigma=1.5)
    assert nf.name == "Normal (gaussian) noise fault"
    assert nf.mu == 0.5
    assert nf.sigma == 1.5

def test_normal_noise_fault_init_checks_numeric_input():
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_numeric_input") as chk:
        NormalNoiseFault(mu=1.0, sigma=2.0)
        assert chk.call_count == 2
        chk.assert_any_call(1.0, 'mu')
        chk.assert_any_call(2.0, 'sigma')

# -------------------------------------------------------------------------
# Noise Generation Tests
# -------------------------------------------------------------------------

def test_call_generates_correct_length_array():
    nf = NormalNoiseFault(mu=0, sigma=1)
    fault_length = 5
    captured = []

    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=lambda arr: captured.append(arr)):

        nf(fault_length)
        assert len(captured) == 1
        arr = captured[0]
        assert len(arr) == fault_length
        assert np.all(np.isfinite(arr))

def test_call_sets_fault_length_and_fault_values():
    nf = NormalNoiseFault(mu=0, sigma=1)
    captured = []

    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=lambda arr: setattr(nf, "fault_values", arr)):

        result = nf(4)
        assert isinstance(result, np.ndarray)
        assert len(result) == 4
        assert result is nf.fault_values

# -------------------------------------------------------------------------
# Validation Tests
# -------------------------------------------------------------------------

def test_call_checks_fault_length_called():
    nf = NormalNoiseFault(mu=0, sigma=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length") as chk, \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault"):

        nf(7)
        chk.assert_called_once_with(7)

# -------------------------------------------------------------------------
# List Output Tests
# -------------------------------------------------------------------------

def test_list_output_returns_list():
    nf = NormalNoiseFault(mu=0, sigma=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault._list_output") as lo:

        lo.return_value = ["a", "b"]
        result = nf(2, list_output=True)
        lo.assert_called_once()
        assert result == ["a", "b"]

def test_list_output_skips_update_fault():
    nf = NormalNoiseFault(mu=0, sigma=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault") as uf, \
         patch("fault_injector.fault_lib.base_fault.BaseFault._list_output"):

        nf(3, list_output=True)
        uf.assert_not_called()

# -------------------------------------------------------------------------
# Edge Case Tests
# -------------------------------------------------------------------------

def test_zero_length_rejected():
    nf = NormalNoiseFault(mu=0, sigma=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length") as chk:
        chk.side_effect = ValueError("invalid length")
        with pytest.raises(ValueError):
            nf(0)

def test_negative_length_rejected():
    nf = NormalNoiseFault(mu=0, sigma=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length") as chk:
        chk.side_effect = ValueError("invalid length")
        with pytest.raises(ValueError):
            nf(-10)

# -------------------------------------------------------------------------
# Randomness Tests
# -------------------------------------------------------------------------

def test_call_returns_different_values_on_multiple_calls():
    nf = NormalNoiseFault(mu=0, sigma=1)
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"):

        vals1 = nf(5)
        vals2 = nf(5)
        assert not np.allclose(vals1, vals2)
