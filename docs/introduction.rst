Introduction
============

**Fault Injector**

A Python package for injecting various faults into numeric time-series or sensor data.

This package allows simulation of real-world sensor anomalies including
drift, offset, noise, missing data, and stuck readings. Faults can be
applied over a specified range of indices.

Supported Fault Types & Mathematical Background
-----------------------------------------------

1. **Drift**

   Linear change over time:

   .. math::

       y_i = x_i + (i - s) \cdot \text{drift_rate}, \quad i \in [s, e)

   - :math:`\text{drift_rate}` can be provided or randomly generated as
     :math:`\text{drift_rate} \sim U(0, 0.0001) \cdot d \cdot \bar{x}`
   - :math:`d` = fault direction (+1 increasing, -1 decreasing)
   - :math:`\bar{x}` = mean of original values

2. **Offset**

   Constant bias added to the values:

   .. math::

       y_i = x_i + \text{offset_value}, \quad i \in [s, e)

   - :math:`\text{offset_value} = \bar{x} \cdot \text{offset_rate}`

3. **Gaussian Noise**

   Random noise with normal distribution:

   .. math::

       y_i = x_i + \epsilon_i, \quad \epsilon_i \sim \mathcal{N}(\mu, \sigma^2), \quad i \in [s, e)

   - Defaults: :math:`\mu = 0`, :math:`\sigma = \text{std}(x[s:e])`

4. **Uniform Noise**

   Random noise with uniform distribution:

   .. math::

       y_i = x_i + \epsilon_i, \quad \epsilon_i \sim U(a, b), \quad i \in [s, e)

   - Defaults: :math:`a = -\text{std}(x[s:e]), b = \text{std}(x[s:e])`

5. **NaN**

   Replace values with missing data:

   .. math::

       y_i =
       \begin{cases}
       \text{NaN}, & i \in [s, e) \\
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

   - :math:`c` can be specified or randomly generated as
     :math:`c = \bar{x} + d \cdot U(0.01, 0.1) \cdot \bar{x}`

Notes
-----

- Faults are applied over the range [start, stop).
- The class preserves the original values for comparison.
- Useful for testing robustness of sensor data processing algorithms,
  anomaly detection, and fault-tolerant systems.

Related Paper
-------------

For more details, see `The Impact of Sensor Faults on Condition Monitoring of a Hydraulic Actuator <https://papers.phmsociety.org/index.php/phmconf/article/view/4415>`_.
