Normal Noise Fault
==================

Define Fault
------------

A **normal noise fault** models a sensor degradation where measurements
are corrupted by random noise drawn from a normal (Gaussian)
distribution. Unlike deterministic faults such as bias or drift, this
fault introduces stochastic fluctuations that reduce signal quality
without introducing a systematic offset.

Let :math:`\epsilon_i \sim \mathcal{N}(\mu, \sigma^2)` denote the additive
noise applied to the sensor signal during the fault interval. The
parameters :math:`\mu` and :math:`\sigma` represent the noise mean and
standard deviation, respectively.

Normal noise faults commonly arise from electromagnetic interference,
thermal noise, vibration, or partial hardware degradation.

Math Behind Fault
-----------------

Assume a univariate time series of true sensor values:

- **True signal:** :math:`x_i`, for index :math:`i = 0, 1, ..., N-1`
- **Fault start index:** :math:`s`
- **Fault end index:** :math:`e`

Linear Normal Noise Model
-------------------------

The observed (faulty) signal :math:`y_i` is defined as:

.. math::

   y_i =
   \begin{cases}
   x_i + \epsilon_i, & s \le i < e \\
   x_i, & \text{otherwise}
   \end{cases}

The noise term is independently sampled at each time step:

.. math::

   \epsilon_i \sim \mathcal{N}(\mu, \sigma^2)

By default, the noise parameters are:

.. math::

   \mu = 0, \qquad \sigma = \mathrm{std}(x_s, x_{s+1}, \ldots, x_{e-1})


Key Takeaway
------------

Normal noise faults degrade signal quality by increasing randomness
rather than shifting the signal systematically.

Example
-------

An example of a normal noise fault compared to the true values is shown
below:

.. image:: ../../images/demos/normal_noise_fault/comparison.png
   :alt: Normal noise fault example

References
----------

- NumPy `normal` random generator:
  `https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html <https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html>`_
