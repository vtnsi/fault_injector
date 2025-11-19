# -*- coding: utf-8 -*-
"""
Normal (gaussian) noise fault class
"""
import numpy as np
from fault_injector.fault_lib.base_fault import BaseFault


class NormalNoiseFault(BaseFault):
    r"""
    Normal Noise Fault
    ==================
    A fault that injects **Gaussian (normal) distributed noise** into a signal.
    This simulates random measurement noise, environmental disturbances, and
    natural sensor variability.

    The noise is drawn i.i.d. from a normal distribution:

    .. math::

        \epsilon_i \sim \mathcal{N}(\mu, \sigma^2)

    and the resulting fault values are:

    .. math::

        y_i = \epsilon_i, \qquad i \in [0, \text{fault\_length})

    This class generates *only* the noise itself.
    When used inside an :class:`Injector`, the noise is **added** to the original
    sensor values as:

    .. math::

        y_i = x_i + \epsilon_i

    (The injector performs the addition.)

    .. admonition:: Statistical Impact

        For a region where original values are :math:`x_i` and fault noise
        :math:`\epsilon_i \sim \mathcal{N}(\mu, \sigma^2)`:

        **Mean Shift**

        .. math::

            \mathbb{E}[y_i] = \bar{x} + \mu

        **Variance Increase**

        Because variance of independent sums adds:

        .. math::

            \mathrm{Var}(y_i)
            = \mathrm{Var}(x_i) + \sigma^2

        Thus, Gaussian noise increases variance and (optionally) shifts the mean.

    Notes
    -----
    This fault type is commonly used to model:

    - electrical interference in analog sensors
    - quantization noise
    - thermal noise in electronics
    - general random jitter

    It is also useful for robustness testing and stress-testing models against
    noisy data.
    """

    def __init__(self, mu, sigma):
        r"""
        Initialize a Gaussian noise fault.

        Parameters
        ----------
        mu : float
            Mean of the Gaussian noise distribution.

        sigma : float
            Standard deviation of the Gaussian noise distribution.
            Must be non-negative.

        Notes
        -----
        Large values of ``sigma`` produce stronger perturbations and can be
        used to simulate degraded sensors or harsh operating environments.
        """
        name = 'Normal (gaussian) noise fault'
        super().__init__(name=name)
        super()._check_numeric_input(mu, 'mu')
        super()._check_numeric_input(sigma, 'sigma')

        self.mu = mu
        self.sigma = sigma


    def __call__(self, fault_length, list_output=False):
        r"""
        Generate a sequence of Gaussian noise values.

        Parameters
        ----------
        fault_length : int
            Number of noise samples to generate.

        list_output : bool, optional
            Whether to return a list instead of a numpy array.
            Defaults to ``False``.

        Returns
        -------
        numpy.ndarray or list
            Random samples drawn from :math:`\mathcal{N}(\mu, \sigma^2)`.

        Notes
        -----
        The injector will *add* these values to the underlying signal.
        Calling this method alone returns the noise itself.
        """
        super()._check_fault_length(fault_length)
        fault_values = np.random.normal(self.mu, self.sigma, fault_length)

        if list_output:
            return super()._list_output(fault_values)
        super().update_fault(fault_values)
        return self.fault_values