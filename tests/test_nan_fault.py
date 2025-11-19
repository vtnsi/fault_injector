import pytest
import numpy as np
from unittest.mock import patch
from fault_injector.fault_lib.nan_fault import NaNFault

# -------------------------------------------------------------------------
# Constructor Tests
# -------------------------------------------------------------------------

def test_nan_fault_init_sets_name():
    nf = NaNFault()
    assert nf.name == "nan fault"
    assert nf.fault_values is None
    assert nf.fault_length is None

# -------------------------------------------------------------------------
# NaN Generation Tests
# -------------------------------------------------------------------------

def test_call_generates_nan_array():
    nf = NaNFault()
    captured = []

    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault", side_effect=lambda arr: captured.append(arr)):

        nf(5)
        assert len(captured) == 1
        result = captured[0]
        assert isinstance(result, np.ndarray)
        assert result.shape == (5,)
        assert np.all(np.isnan(result))

def test_call_sets_fault_length():
    nf = NaNFault()
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault"):

        nf(4)
        assert nf.fault_length == 4

# -------------------------------------------------------------------------
# Validation / Utils Call Tests
# -------------------------------------------------------------------------

def test_call_checks_fault_length_called():
    nf = NaNFault()
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length") as chk, \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault"):

        nf(7)
        chk.assert_called_once_with(7)

# -------------------------------------------------------------------------
# List Output Tests
# -------------------------------------------------------------------------

def test_list_output_returns_list():
    nf = NaNFault()
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault._list_output") as lo:

        lo.return_value = ["a", "b"]
        result = nf(2, list_output=True)
        lo.assert_called_once()
        assert result == ["a", "b"]

def test_list_output_skips_update_fault():
    nf = NaNFault()
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault") as uf, \
         patch("fault_injector.fault_lib.base_fault.BaseFault._list_output"):

        nf(3, list_output=True)
        uf.assert_not_called()

# -------------------------------------------------------------------------
# Returned Array Tests
# -------------------------------------------------------------------------

def test_call_returns_internal_fault_values():
    nf = NaNFault()
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length"), \
         patch("fault_injector.fault_lib.base_fault.BaseFault.update_fault") as uf:

        uf.side_effect = lambda arr: setattr(nf, "fault_values", arr)
        result = nf(3)
        assert isinstance(result, np.ndarray)
        assert result is nf.fault_values
        assert np.all(np.isnan(result))

# -------------------------------------------------------------------------
# Edge Case Tests
# -------------------------------------------------------------------------

def test_zero_length_rejected():
    nf = NaNFault()
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length") as chk:
        chk.side_effect = ValueError("invalid length")
        with pytest.raises(ValueError):
            nf(0)

def test_negative_length_rejected():
    nf = NaNFault()
    with patch("fault_injector.fault_lib.base_fault.BaseFault._check_fault_length") as chk:
        chk.side_effect = ValueError("invalid length")
        with pytest.raises(ValueError):
            nf(-5)
