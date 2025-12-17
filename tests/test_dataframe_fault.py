import numpy as np
import pytest
from fault_injector import DataFrameFault
from fault_injector.fault_lib import DriftFault, StuckValueFault

# Horizontal generation

def test_horizontal_generation_basic():
    df_fault = DataFrameFault(
        col_names=["A", "B"],
        horizontal=True,
        df_length=3,
        fault_length=3
    )
    df_fault.assign_fault("A", StuckValueFault, {"stuck_val": 5})
    df_fault.assign_fault("B", DriftFault, {"drift_rate": 1, "continuous": False})

    df_final = df_fault.generate_faults()
    for arr in df_final["A"]:
        assert np.all(arr == 5)

    expected = [np.array([1, 2, 3])] * 3
    for arr, exp in zip(df_final["B"], expected):
        assert np.array_equal(arr, exp)


def test_continuous_fault_accumulates():
    df_fault = DataFrameFault(
        col_names=["B"],
        horizontal=True,
        df_length=4,
        fault_length=3
    )
    df_fault.assign_fault("B", DriftFault, {"drift_rate": 1, "continuous": True})

    df_final = df_fault.generate_faults()
    expected = [
        np.array([1, 2, 3]),
        np.array([4, 5, 6]),
        np.array([7, 8, 9]),
        np.array([10, 11, 12])
    ]
    for arr, exp in zip(df_final["B"], expected):
        assert np.array_equal(arr, exp)


def test_persistence_flag():
    df_fault = DataFrameFault(
        col_names=["B"],
        horizontal=True,
        df_length=3,
        fault_length=2
    )
    df_fault.assign_fault("B", DriftFault, {"drift_rate": 1, "continuous": True}, persist_state=True)

    first_call = df_fault.generate_faults()
    second_call = df_fault.generate_faults()

    first_vals = [arr.tolist() for arr in first_call["B"]]
    second_vals = [arr.tolist() for arr in second_call["B"]]

    # confirm drift continues across calls
    assert first_vals[-1] == [5, 6]  # adjusted to correct indices
    assert second_vals[0] == [7, 8]


def test_reset_when_nonpersistent():
    df_fault = DataFrameFault(
        col_names=["B"],
        horizontal=True,
        df_length=2,
        fault_length=2
    )
    df_fault.assign_fault("B", DriftFault, {"drift_rate": 1, "continuous": True}, persist_state=False)

    first_call = df_fault.generate_faults()
    second_call = df_fault.generate_faults()
    for a1, a2 in zip(first_call["B"], second_call["B"]):
        assert np.array_equal(a1, a2)


# Vertical generation

def test_vertical_generation_basic():
    df_fault = DataFrameFault(
        col_names=["A", "B"],
        horizontal=False,
        df_length=4
    )
    df_fault.assign_fault("A", StuckValueFault, {"stuck_val": 3})
    df_fault.assign_fault("B", DriftFault, {"drift_rate": 2, "continuous": False})

    df_final = df_fault.generate_faults()
    assert np.all(df_final["A"] == 3)
    expected = np.array([2, 4, 6, 8])  # matches vertical drift formula
    assert np.array_equal(df_final["B"], expected)


# Multi-fault & param tests

def test_multi_fault_combination():
    df_fault = DataFrameFault(
        col_names=["A"],
        horizontal=True,
        df_length=2,
        fault_length=2,
        multi_fault=True
    )
    df_fault.assign_fault("A", StuckValueFault, {"stuck_val": 1})
    df_fault.assign_fault("A", StuckValueFault, {"stuck_val": 2})

    df_final = df_fault.generate_faults()
    expected = [np.array([3, 3]), np.array([3, 3])]
    for arr, exp in zip(df_final["A"], expected):
        assert np.array_equal(arr, exp)


def test_param_broadcasting_repeat():
    df_fault = DataFrameFault(
        col_names=["A"],
        horizontal=True,
        df_length=4,
        fault_length=2
    )
    df_fault.assign_fault("A", StuckValueFault, {"stuck_val": [1, 2]}, repeat=True)

    df_final = df_fault.generate_faults()
    expected = [
        np.array([1, 1]),
        np.array([2, 2]),
        np.array([2, 2]),
        np.array([2, 2])
    ]
    for arr, exp in zip(df_final["A"], expected):
        assert np.array_equal(arr, exp)
