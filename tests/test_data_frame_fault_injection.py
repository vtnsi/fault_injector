import pandas as pd
import numpy as np
import pytest
from fault_injector.injector import FaultInjection
from fault_injector.data_frame_injector import DataFrameFaultInjection


# Constructor tests
def test_init_basic():
    df = pd.DataFrame({"A": [1, 2, 3, 4]})
    dfi = DataFrameFaultInjection(df, "A", 1, 3)

    assert dfi.column_names == ["A"]
    assert dfi.start_val == 1
    assert dfi.stop_val == 3
    assert "A" not in dfi.fault_dict
    assert dfi.original_df.equals(df)
    assert dfi.fault_df.equals(df)


def test_init_multiple_columns():
    df = pd.DataFrame({"A": [1,2,3], "B": [4,5,6]})
    dfi = DataFrameFaultInjection(df, ["A", "B"], 0, 2)

    assert dfi.column_names == ["A", "B"]
    assert dfi.start_val == 0
    assert dfi.stop_val == 2


# inject_fault() tests
def test_inject_fault_creates_dict_of_fault_objects():
    df = pd.DataFrame({"A": [10, 20, 30], "B": [5, 6, 7]})
    dfi = DataFrameFaultInjection(df, ["A", "B"], 0, 2)

    fault_dict = dfi.inject_fault()

    assert isinstance(fault_dict, dict)
    assert "A" in fault_dict
    assert "B" in fault_dict

    # ensure objects are FaultInjection instances
    assert isinstance(fault_dict["A"], FaultInjection)
    assert isinstance(fault_dict["B"], FaultInjection)

    # ensure FaultInjection got the correct values
    assert fault_dict["A"].values == [10, 20, 30]
    assert fault_dict["B"].values == [5, 6, 7]

    # ensure start/stop were passed correctly
    assert fault_dict["A"].start == 0
    assert fault_dict["A"].stop == 2


# update_df() tests
def test_update_df_applies_faults():
    df = pd.DataFrame({"A": [1, 1, 1, 1]})
    dfi = DataFrameFaultInjection(df, "A", 1, 3)

    # manual: inject a drift fault for consistency
    dfi.inject_fault()
    fi_obj = dfi.fault_dict["A"]
    fi_obj.inject_drift(drift_rate=1.0)   # ensures predictable change

    updated_df = dfi.update_df()

    # Value changes only between index 1 and 2
    expected = pd.DataFrame({"A": [1, 2, 3, 1]})

    assert updated_df["A"].tolist() == expected["A"].tolist()


def test_full_multi_column_integration():
    df = pd.DataFrame({
        "A": [10, 10, 10, 10],
        "B": [20, 20, 20, 20],
        "C": [30, 30, 30, 30]
    })

    dfi = DataFrameFaultInjection(df, ["A", "C"], 1, 3)
    dfi.inject_fault()

    # Apply different faults to each column manually (consistent testing)
    dfi.fault_dict["A"].inject_offset(0.1)  # offset based on mean
    dfi.fault_dict["C"].inject_stuck_value(99)

    updated = dfi.update_df()

    # A gets offset: mean(A)=10 -> offset=1.0 -> indexes 1,2 are 11
    expected_A = [10, 11, 11, 10]
    # C becomes stuck at 99 at indexes 1 and 2
    expected_C = [30, 99, 99, 30]

    assert updated["A"].tolist() == expected_A
    assert updated["C"].tolist() == expected_C
    assert updated["B"].tolist() == [20, 20, 20, 20]  # untouched
