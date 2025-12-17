import numpy as np
import pandas as pd
import pytest
from fault_injector import Injector, DataFrameFault, DataFrameInjector


def test_horizontal_basic_injection():
    df = pd.DataFrame({
        "A": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "B": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    })
    faulty = pd.DataFrame({
        "A": [[5, 5, 5], [9, 9, 9], [7, 7, 7]],
        "B": [[2, 2, 2], [4, 4, 4], [6, 6, 6]]
    })

    inj = DataFrameInjector(df)
    out = inj.inject_faults(faulty)

    for arr, expected in zip(out["A"], faulty["A"]):
        assert np.array_equal(arr, expected)

    for arr, expected in zip(out["B"], faulty["B"]):
        assert np.array_equal(arr, expected)


def test_horizontal_partial_range():
    df = pd.DataFrame({
        "A": [[1, 2], [1, 2], [1, 2], [1, 2]],
    })
    faulty = pd.DataFrame({
        "A": [[9, 9], [8, 8]],
    })

    inj = DataFrameInjector(df)
    out = inj.inject_faults(faulty, start=1, stop=3)

    # rows 1 and 2 replaced
    assert np.array_equal(out.at[1, "A"], np.array([9, 9]))
    assert np.array_equal(out.at[2, "A"], np.array([8, 8]))

    # rows 0 and 3 unchanged
    assert np.array_equal(out.at[0, "A"], np.array([1, 2]))
    assert np.array_equal(out.at[3, "A"], np.array([1, 2]))


def test_horizontal_add_mode():
    df = pd.DataFrame({
        "A": [[10, 20], [10, 20], [10, 20]]
    })
    faulty = pd.DataFrame({
        "A": [[1, 1], [2, 2], [3, 3]]
    })

    inj = DataFrameInjector(df)
    out = inj.inject_faults(faulty, replace=False)

    expected = [
        np.array([11, 21]),
        np.array([12, 22]),
        np.array([13, 23]),
    ]

    for arr, exp in zip(out["A"], expected):
        assert np.array_equal(arr, exp)


def test_vertical_basic():
    df = pd.DataFrame({
        "A": [10, 20, 30, 40],
        "B": [0, 1, 2, 3],
    })

    faulty = pd.DataFrame({
        "A": [100, 200, 300, 400],
        "B": [9, 9, 9, 9],
    })

    inj = DataFrameInjector(df)
    out = inj.inject_faults(faulty)

    assert np.array_equal(out["A"].values, [100, 200, 300, 400])
    assert np.array_equal(out["B"].values, [9, 9, 9, 9])


def test_vertical_partial_range():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5]
    })

    faulty = pd.DataFrame({
        "A": [99, 88]
    })

    inj = DataFrameInjector(df)
    out = inj.inject_faults(faulty, start=1, stop=3)

    assert np.array_equal(out["A"].values,
                          [1, 99, 88, 4, 5])


def test_vertical_add_mode():
    df = pd.DataFrame({"X": [10, 20, 30]})
    faulty = pd.DataFrame({"X": [1, 1, 1]})

    inj = DataFrameInjector(df)
    out = inj.inject_faults(faulty, replace=False)

    assert np.array_equal(out["X"].values, [11, 21, 31])


def test_column_map():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [10, 20, 30],
    })
    faulty = pd.DataFrame({
        "FA": [100, 200, 300],
        "FB": [9, 9, 9],
    })

    inj = DataFrameInjector(df)
    out = inj.inject_faults(
        faulty_df=faulty,
        columns_to_inject=["A", "B"],
        column_map={"A": "FA", "B": "FB"}
    )

    assert np.array_equal(out["A"].values, [100, 200, 300])
    assert np.array_equal(out["B"].values, [9, 9, 9])


def test_length_mismatch_raises():
    df = pd.DataFrame({
        "A": [[1, 1], [1, 1], [1, 1]]
    })
    faulty = pd.DataFrame({
        "A": [[9, 9], [8, 8]]
    })

    inj = DataFrameInjector(df)
    with pytest.raises(ValueError):
        inj.inject_faults(faulty)


def test_horizontal_misaligned_array_raises():
    df = pd.DataFrame({
        "A": [[1, 2], [1, 2]]
    })
    faulty = pd.DataFrame({
        "A": [[9, 9, 9], [8, 8, 8]]
    })

    inj = DataFrameInjector(df)
    with pytest.raises(ValueError):
        inj.inject_faults(faulty)


def test_incompatible_horizontal_vertical_mix():
    df = pd.DataFrame({
        "A": [10, 20, 30]
    })
    faulty = pd.DataFrame({
        "A": [[1, 2], [3, 4], [5, 6]]
    })

    inj = DataFrameInjector(df)
    with pytest.raises(TypeError):
        inj.inject_faults(faulty)
