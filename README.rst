nameko-structlog
================


Structlog as nameko extension


* Free software: Apache Software License 2.0


Extension for `nameko <https://www.nameko.io>`_ that replaces python logging module with structlog.
The idea behind this module is to use `JSONRenderer <https://www.structlog.org/en/stable/api.html#structlog.processors.JSONRenderer>`_
to be able to use advanced log aggregation and analysis tools like `Logstash <https://www.elastic.co/products/logstash>`_.

Apart from JSONRenderer structlog processor, it's also supported `KeyValueRenderer <https://www.structlog.org/en/stable/api.html#structlog.processors.KeyValueRenderer>`_
processor.


Installation
------------

To install nameko-structlog, simply use pip.

.. code-block:: bash

   pip install nameko-structlog


Usage
-----

Add Structlog log level to your nameko config file:

.. code-block:: yaml

   # config.yml when using JSONRenderer
   STRUCTLOG:
      INCLUDE_WORKER_NAME: ${INCLUDE_WORKER_NAME:true}
      INCLUDE_LOG_TRANSACTON_ID: true
      PROCESSOR_NAME: JSONRenderer
      PROCESSOR_OPTIONS:
        sort_keys: true
      EXTRA_PARAMETERS:
         pin: 1234
         env: dev

  LOGGING:
    version: 1
    formatters:
      simple:
        format: "%(message)s"

    handlers:
      console:
        class: logging.StreamHandler
        formatter: simple

    root:
      level: DEBUG
      handlers: [console]
   ...

Option *INCLUDE_WORKER_NAME* will add or not *worker_ctx.call_id* to
every log entry. Option *INCLUDE_LOG_TRANSACTON_ID* will group all
logs that refer to same nameko entrypoint, with a unique *log_transaction_id*.
Doing so may be useful to follow request/data flow on a log aggregation
tool. Option *EXTRA_PARAMETERS* can contain any keys that you
want to appear on every log entry.


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
         self.log.info(message=f"Your name is {name}", type="greeting")


Run your service, providing the config file:

.. code-block:: shell

   $ nameko run service --config config.yaml

   $ nameko shell --config config.yaml
   >>> n.rpc.demo.my_method("Alice")
   {"level": "info", "log_transaction_id": "b2cd5506-339e-4e59-9a14-a3cd7548bfe5", "logger": "demo", "env": "dev", message": "Your name is Alice", "pin": "1234", "timestamp": "2020-09-27T11:24:30.379918Z", "type": "greeting"}


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
