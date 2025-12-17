import numpy as np
import pandas as pd
import pytest
from fault_injector.df_injector import DataFrameInjector

# Helper / mock fault classes
class DummyFault:
    """Simple fault that returns input unchanged"""
    def inject_fault(self, x):
        return x


class AddOneFault:
    """Adds 1 to every element"""
    def inject_fault(self, x):
        return x + 1


class BadFaultClass:
    """Used to test passing a class instead of an instance"""
    def inject_fault(self, x):
        return x

# Constructor tests
def test_valid_injector_dict():
    inj = DataFrameInjector(
        injector_dict={"A": DummyFault()}
    )
    assert isinstance(inj.injector_dict, dict)


def test_injector_dict_not_dict_raises():
    with pytest.raises(ValueError, match="injector_dict must be a dictionary"):
        DataFrameInjector(injector_dict=["not", "a", "dict"])


def test_fault_class_instead_of_instance_raises():
    with pytest.raises(TypeError, match="Expected a fault instance"):
        DataFrameInjector(
            injector_dict={"A": BadFaultClass}
        )

# inject_faults behavior tests
def test_single_column_injection():
    df = pd.DataFrame({
        "A": [1, 2, 3]
    })

    inj = DataFrameInjector(
        injector_dict={"A": AddOneFault()}
    )

    out = inj.inject_faults(df)

    assert np.array_equal(out["A"].values, [2, 3, 4])


def test_multiple_column_injection():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [10, 20, 30],
    })

    inj = DataFrameInjector(
        injector_dict={
            "A": AddOneFault(),
            "B": DummyFault(),
        }
    )

    out = inj.inject_faults(df)

    assert np.array_equal(out["A"].values, [2, 3, 4])
    assert np.array_equal(out["B"].values, [10, 20, 30])


def test_original_dataframe_not_modified():
    df = pd.DataFrame({"A": [1, 2, 3]})
    inj = DataFrameInjector({"A": AddOneFault()})

    _ = inj.inject_faults(df)

    assert np.array_equal(df["A"].values, [1, 2, 3])

# DataFrame validation tests
def test_missing_column_raises():
    df = pd.DataFrame({"A": [1, 2, 3]})

    inj = DataFrameInjector(
        injector_dict={"B": DummyFault()}
    )

    with pytest.raises(TypeError, match="NOT present in df columns"):
        inj.inject_faults(df)


def test_non_numeric_column_raises():
    df = pd.DataFrame({
        "A": ["x", "y", "z"]
    })

    inj = DataFrameInjector(
        injector_dict={"A": DummyFault()}
    )

    with pytest.raises(ValueError, match="must contain numeric values"):
        inj.inject_faults(df)


def test_non_ndarray_values_raises():
    # Force object dtype that becomes non-numeric ndarray
    df = pd.DataFrame({
        "A": [["a"], ["b"], ["c"]]
    })

    inj = DataFrameInjector(
        injector_dict={"A": DummyFault()}
    )

    with pytest.raises(ValueError):
        inj.inject_faults(df)

# Fault instance validation during injection
def test_fault_instance_checked_at_injection_time():
    df = pd.DataFrame({"A": [1, 2, 3]})

    inj = DataFrameInjector(
        injector_dict={"A": DummyFault()}
    )

    # Break the injector_dict after construction
    inj.injector_dict["A"] = BadFaultClass

    with pytest.raises(TypeError, match="Expected a fault instance"):
        inj.inject_faults(df)
