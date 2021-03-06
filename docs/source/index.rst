.. -*- mode: rst -*-

.. image:: https://travis-ci.org/EtienneCmb/tensorpac.svg?branch=master
    :target: https://travis-ci.org/EtienneCmb/tensorpac

.. image:: https://codecov.io/gh/EtienneCmb/tensorpac/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/EtienneCmb/tensorpac

.. image:: https://badge.fury.io/py/Tensorpac.svg
    :target: https://badge.fury.io/py/Tensorpac

Tensorpac
#########

Tensorpac is an open-source Python toolbox for computing Phase-Amplitude Coupling (PAC) using tensors and parallel computing. This software provides a modular implementation which allows one to combine existing methods for measuring PAC and chance distribution.
To get started, see our `examples <https://github.com/EtienneCmb/tensorpac/tree/master/examples>`_.

.. figure::  picture/tp.png
   :align:   center

Installation:
*************

Tensorpac is based on NumPy (>=1.12), SciPy and uses `Joblib <https://pythonhosted.org/joblib/>`_ for parallel computing. To install Tensorpac, just open a terminal and run :

.. code-block:: bash

    pip install tensorpac

What's new?
***********

* New in version v0.5.2
    
    * :ref:`erpac` (Voytek et al. 2013)
    * pip installation

* New in version v0.5.1
    
    * Compute and plot :ref:`pp`
    * Bug fixing

Todo list
*********

.. todo::

    * Generalized Linear Model (GLM - Lakatos, 2005)
    * PAC using PSD
    * Morse's wavelets

Contents:
*********

.. toctree::
   :maxdepth: 3

   methods
   api
   auto_examples/index.rst

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

