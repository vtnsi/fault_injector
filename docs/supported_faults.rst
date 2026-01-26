Supported Fault Types & Mathematical Background
===============================================

1. **Drift**

   Linear change over time:

   .. math::

       y_i = x_i + (i - s)\, r, \quad i \in [s, e)

   - :math:`r \in \mathbb{R}` is the drift rate
   - By default: :math:`r \sim \mathcal{U}(0, 0.0001)\, d\, \bar{x}`
   - :math:`d \in \{-1, 1\}` controls the drift direction
   - :math:`\bar{x}` is the mean of the original signal over the fault interval

2. **Offset**

   Constant bias added to the values:

   .. math::

       y_i = x_i + b, \quad i \in [s, e)

   - :math:`b = r\, \bar{x}` is the offset magnitude
   - :math:`r \in \mathbb{R}` is the offset rate

3. **Gaussian Noise**

   Random noise with a normal distribution:

   .. math::

       y_i = x_i + \epsilon_i, \quad
       \epsilon_i \sim \mathcal{N}(\mu, \sigma^2), \quad i \in [s, e)

   - Defaults: :math:`\mu = 0`
   - :math:`\sigma` is the standard deviation of the signal over the fault interval

4. **Uniform Noise**

   Random noise with a uniform distribution:

   .. math::

       y_i = x_i + \epsilon_i, \quad
       \epsilon_i \sim \mathcal{U}(a, b), \quad i \in [s, e)

   - Defaults: :math:`a = -\sigma`, :math:`b = \sigma`
   - :math:`\sigma` is the standard deviation of the signal over the fault interval

5. **NaN**

   Replace values with missing data:

   .. math::

       y_i =
       \begin{cases}
       \mathrm{NaN}, & i \in [s, e) \\
       x_i, & \text{otherwise}
       \end{cases}

6. **Stuck Value**

   Replace values with a constant:

   .. math::

       y_i =
       \begin{cases}
       c, & i \in [s, e) \\
       x_i, & \text{otherwise}
       \end{cases}

   - :math:`c` may be specified directly or generated as
     :math:`c = \bar{x}\left(1 + d\, u\right)`
   - :math:`u \sim \mathcal{U}(0.01, 0.1)`

Notes
-----

- Faults are applied over the range [start, stop).
- The class preserves the original values for comparison.
- Useful for testing robustness of sensor data processing algorithms,
  anomaly detection, and fault-tolerant systems.
