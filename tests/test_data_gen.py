import pytest
import numpy as np
from fault_injector.generate_data import DataGen


def test_init_valid_inputs():
    dg = DataGen(rand_max=10, rand_min=2, size=5)

    assert dg.rand_max == 10
    assert dg.rand_min == 2
    assert dg.size == 5
    assert dg.values == []


def test_init_invalid_rand_max():
    with pytest.raises(ValueError):
        DataGen(rand_max="bad", rand_min=0, size=10)


def test_init_invalid_rand_min():
    # not numeric
    with pytest.raises(ValueError):
        DataGen(rand_max=10, rand_min="bad", size=10)

    # >= rand_max
    with pytest.raises(ValueError):
        DataGen(rand_max=10, rand_min=20, size=10)


def test_init_invalid_size():
    with pytest.raises(ValueError):
        DataGen(rand_max=10, rand_min=1, size=0)

    with pytest.raises(ValueError):
        DataGen(rand_max=10, rand_min=1, size=-5)

    with pytest.raises(ValueError):
        DataGen(rand_max=10, rand_min=1, size="bad")


def test_random_gen_creates_correct_size():
    dg = DataGen(rand_max=10, rand_min=5, size=4)
    dg.random_gen()

    assert len(dg.values) == 4


def test_random_gen_values_within_range():
    dg = DataGen(rand_max=10, rand_min=5, size=100)
    dg.random_gen()

    assert all(5 <= v <= 10 for v in dg.values)


def test_random_gen_appends_not_overwrites():
    dg = DataGen(rand_max=10, rand_min=5, size=3)

    dg.random_gen()
    first_vals = dg.values.copy()

    dg.random_gen()
    second_vals = dg.values

    assert len(second_vals) == 6            # appended again
    assert first_vals == second_vals[:3]    # original values preserved


def test_plot_values_runs_without_error(monkeypatch):
    """
    Ensures no exceptions occur during plotting.
    Monkeypatches plt.show() so the test does not display a window.
    """

    import matplotlib.pyplot as plt

    # prevent plot window from popping up
    monkeypatch.setattr(plt, "show", lambda: None)

    dg = DataGen(rand_max=10, rand_min=5, size=3)
    dg.random_gen()

    # Should not throw
    dg.plot_values()
