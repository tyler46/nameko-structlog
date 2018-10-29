nameko-structlog
================


Structlog as nameko extension


* Free software: Apache Software License 2.0


Extension for `nameko <https://www.nameko.io>`_ that replaces python logging module with structlog.

Installation
------------

To install nameko-structlog, simply use pip.

.. code-block:: bash

   pip install nameko-structlog
   # to enable coloring during development
   pip install nameko-structlog[colors]


Usage
-----

Add Structlog log level to your nameko config file:

.. code-block:: yaml

   # config.yml
   STRUCTLOG:
      DEVELOPMENT_MODE: ${DEV:false}
      WORKER_NAME: ${WORKER_NAME:false}

   ...


Include the ``StructlogDependency`` dependency in your service class:

.. code-block:: python 

   # service.py
   from nameko.rpc import rpc 
   
   from nameko_structlog import StructlogDependency

   class MyService(object):
      name = 'demo'

      log = StructlogDependency()

      @rpc 
      def my_method(self, name):
         self.log.info('Your name is '.format(name))


Run your service, providing the config file:

.. code-block:: shell

   $ nameko run service --config config.yaml


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
