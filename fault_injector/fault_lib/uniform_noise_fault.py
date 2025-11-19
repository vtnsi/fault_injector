# -*- coding: utf-8 -*-
"""
uniform noise fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault


class UniformNoiseFault(BaseFault):
    r"""
    Injects **uniform random noise** into the signal over the specified fault range.

    This simulates measurement noise, sensor jitter, or environmental interference
    where samples fluctuate randomly within a fixed minimum–maximum range.

    .. rubric:: Parameters

    **min_val** : *float*
        Lower bound of the uniform noise distribution.

    **max_val** : *float*
        Upper bound of the uniform noise distribution.

    .. admonition:: Math Behind Uniform Noise Fault

        The signal is perturbed by additive uniform noise:

        .. math::
            y_i = x_i + \epsilon_i,
            \qquad \epsilon_i \sim U(a, b), \quad i \in [s, e)

        where:

        - :math:`x_i` = original sample
        - :math:`y_i` = sample after noise injection
        - :math:`a, b` = ``min_val`` and ``max_val``
        - :math:`s` = start index
        - :math:`e` = stop index

        **Impact on Descriptive Statistics (within [s, e))**

        - **Mean Shift:**

          Expected mean shifts by the midpoint of the uniform range:

          .. math::
              \mathbb{E}[\bar{y}_{[s,e)}]
              = \bar{x}_{[s,e)} + \frac{a + b}{2}

        - **Variance Increase:**

          Variance increases by:

          .. math::
              \text{Var}(y_{[s,e)})
              = \text{Var}(x_{[s,e)}) + \frac{(b - a)^2}{12}

        Thus, uniform noise broadens the distribution evenly across the defined
        interval and consistently increases variance.

    Notes
    -----
    Use this fault type to simulate:

    - sensor quantization jitter
    - thermal/environmental fluctuations
    - random analog read noise
    - bounded random interference

    Useful in testing robustness of filters, controllers, and statistical models.
    """

    def __init__(self, min_val, max_val):
        r"""
        Initialize the UniformNoiseFault.

        Parameters
        ----------
        min_val : float
            Lower bound of the uniform noise distribution (a).

        max_val : float
            Upper bound of the uniform noise distribution (b).

        Notes
        -----
        - Both ``min_val`` and ``max_val`` must be numeric. The code does not
          automatically swap values: ensure ``min_val <= max_val`` when calling.
        - The generated noise is sampled from :math:`U(a, b)` and is additive
          when used with an Injector that adds the fault to original values.
        """
        name = 'uniform noise fault'
        super().__init__(name=name)
        super()._check_numeric_input(min_val, 'min_val')
        super()._check_numeric_input(max_val, 'max_val')

        self.min_val = min_val
        self.max_val = max_val


    def __call__(self, fault_length, list_output=False):
        r"""
        Generate uniform random noise of the specified length.

        Parameters
        ----------
        fault_length : int
            Number of noise samples to generate. Must be a positive integer.

        list_output : bool, optional
            If True, returns the generated noise as a Python list (and updates
            internal state via :meth:`_list_output`). If False (default),
            updates internal state and returns a NumPy array.

        Returns
        -------
        numpy.ndarray or list
            Samples drawn from the uniform distribution U(min_val, max_val).

        Notes
        -----
        - The produced sequence represents the additive noise :math:`\epsilon_i`.
          When injected, the injector typically computes :math:`y_i = x_i + \epsilon_i`.
        - If ``min_val == max_val``, the noise reduces to a constant equal to
          that value.
        """
        super()._check_fault_length(fault_length)
        fault_values = np.random.uniform(self.min_val, self.max_val, fault_length)

        if list_output:
            return super()._list_output(fault_values)
        super().update_fault(fault_values)
        return self.fault_values