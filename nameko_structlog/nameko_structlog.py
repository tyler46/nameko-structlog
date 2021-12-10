"""
Nameko Structlog Dependency Provider.
"""
import uuid

import structlog
from nameko.exceptions import ConfigurationError
from nameko.extensions import DependencyProvider

from nameko_structlog.constants import (
    JSON_PROCESSOR,
    INCLUDE_WORKER_NAME_KEY,
    INCLUDE_LOG_TRANSACTION_ID_KEY,
    PARAMETERS_KEY,
    PROCESSOR_NAME_KEY,
    PROCESSOR_OPTIONS_KEY,
    STRUCTLOG_CONFIG_KEY,
    SUPPORTED_PROCESSORS,
)


class StructlogLogger:

    def __init__(
        self,
        processor_name,
        options,
        extra_params,
        worker_ctx,
        include_worker_name=True,
        include_log_transaction_id=True,
    ):
        self.processor = getattr(structlog.processors, processor_name)

        initial_values = extra_params.copy()
        if include_log_transaction_id:
            initial_values.update({"log_transaction_id": self._transaction_id()})
        if include_worker_name:
            initial_values.update({"entrypoint": worker_ctx.call_id})

        self.initial_values = initial_values
        self.service_name = worker_ctx.service_name

        self.chain = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            self.processor(**options),
        ]

    def _transaction_id(self):
        return str(uuid.uuid4())

    def get_logger(self):
        if not structlog.is_configured():
            structlog.configure(
                processors=self.chain,
                context_class=structlog.threadlocal.wrap_dict(dict),
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=True,
            )

        logger = structlog.get_logger(self.service_name).new()
        return logger.bind(**self.initial_values)


class StructlogDependency(DependencyProvider):
    """Dependency Provider of Structlog."""

    def setup(self):
        structlog_config = self.container.config.get(STRUCTLOG_CONFIG_KEY, {})
        self.processor_name = structlog_config.get(PROCESSOR_NAME_KEY, JSON_PROCESSOR)
        if self.processor_name not in SUPPORTED_PROCESSORS:
            raise ConfigurationError(
                "Invalid `{processor_key}` provided. Valid ones are: {supported}.".format(
                    processor_key=PROCESSOR_NAME_KEY,
                    supported=SUPPORTED_PROCESSORS,
                )
            )

        self.processor_options = structlog_config.get(PROCESSOR_OPTIONS_KEY, {})
        self.include_worker_name = structlog_config.get(INCLUDE_WORKER_NAME_KEY, True)
        self.include_log_transaction_id = structlog_config.get(
            INCLUDE_LOG_TRANSACTION_ID_KEY, True
        )
        self.extra_params = structlog_config.get(PARAMETERS_KEY, {})

    def get_dependency(self, worker_ctx):
        return StructlogLogger(
            self.processor_name,
            self.processor_options,
            self.extra_params,
            worker_ctx,
            self.include_worker_name,
            self.include_log_transaction_id,
        ).get_logger()
