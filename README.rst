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
      SORT_KEYS: ${SORT_KEYS:true}
      CUSTOM_KEYS:
         service_name: logger
   ...

CUSTOM_DATA: can contain any key that you want to use in log.



Include the ``StructlogDependency`` dependency in your service class:

.. code-block:: python 

   # service.py
   from nameko.rpc import rpc 
   
   from nameko_structlog import StructlogDependency

   class MyService(object):
      name = "demo"

      log = StructlogDependency()

      @rpc 
      def my_method(self, name):
         self.log.info(message="Your name is {}".format(name), type="greeting")


Run your service, providing the config file:

.. code-block:: shell

   $ nameko run service --config config.yaml

   $ nameko shell --config config.yaml
   >>> n.rpc.demo.my_method("Alice")
   {"level": "info", "log_transaction_id": "b2cd5506-339e-4e59-9a14-a3cd7548bfe5", "logger": "demo", "message": "Your name is Alice", "service_name": "logger", "timestamp": "2020-09-27T11:24:30.379918Z", "type": "greeting"}


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
