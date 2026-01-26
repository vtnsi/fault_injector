Uniform Noise Fault
===================

Define Fault
------------

A **uniform noise fault** models a sensor degradation in which measurements
are corrupted by random noise drawn from a uniform distribution. Unlike
normal (Gaussian) noise, uniform noise introduces equally likely
fluctuations within a bounded range.

Uniform noise faults can arise from quantization effects, sensor
resolution limits, or low-level interference.

Let :math:`\epsilon_i \sim \mathcal{U}(a, b)` denote the additive noise
applied during the fault interval. By default, the bounds :math:`a` and
:math:`b` are defined relative to the signal scale as

.. math::

   a = -\sigma, \qquad b = \sigma

where

.. math::

   \sigma = \sqrt{\frac{1}{e - s} \sum_{i=s}^{e-1} \left(x_i - \bar{x}\right)^2},
   \qquad
   \bar{x} = \frac{1}{e - s} \sum_{i=s}^{e-1} x_i .


Math Behind Fault
-----------------

Assume a univariate time series of true sensor values:

- **True signal:** :math:`x_i`, for index :math:`i = 0, 1, 2, \ldots, N-1`
- **Fault start index:** :math:`s`
- **Fault end index:** :math:`e`

Linear Uniform Noise Model
--------------------------

The observed (faulty) signal :math:`y_i` is defined as:

.. math::

   y_i =
   \begin{cases}
   x_i + \epsilon_i, & s \le i < e \\
   x_i, & \text{otherwise}
   \end{cases}

where :math:`\epsilon_i` is independently sampled from the uniform
distribution :math:`U(a, b)`.


Key Takeaway
------------

Uniform noise faults degrade signal quality by increasing randomness
while preserving the mean.

Example
-------

An example of a uniform noise fault compared to the true values is shown
below:

.. image:: ../../images/demos/uniform_noise_fault/comparison.png
   :alt: Uniform noise fault example

References
----------

- NumPy `uniform` random generator:
  `https://numpy.org/doc/stable/reference/random/generated/numpy.random.uniform.html <https://numpy.org/doc/stable/reference/random/generated/numpy.random.uniform.html>`_
