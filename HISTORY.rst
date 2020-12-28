=======
History
=======

0.2.0 (2020-12-28)
------------------

* Drop `indent=2` for log records
* Drop `colorama` and `development` mode.
* Support two structlog processors, `JSONRenderer <https://www.structlog.org/en/stable/api.html#structlog.processors.JSONRenderer>`_
  and `KeyValueRenderer <https://www.structlog.org/en/stable/api.html#structlog.processors.KeyValueRenderer>`_.
* Configuration is more clean now.
* Decouple Structlog configuration from nameko dependency.

0.1.1 (2018-10-29)
------------------

* First release on PyPI.
