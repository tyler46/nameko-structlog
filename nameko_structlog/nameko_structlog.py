"""
Nameko Structlog Dependency Provider.
"""
import uuid

from nameko.extensions import DependencyProvider

import structlog

try:
    import colorama  # noqa pylint: disable=W0611
except ImportError:
    use_colors = False
else:
    use_colors = True


class StructlogDependency(DependencyProvider):
    """Dependency Provider of Structlog."""

    def setup(self):
        structlog_config = self.container.config.get("STRUCTLOG", {})
        self.development_mode = structlog_config.get("DEVELOPMENT_MODE", False)
        self.include_worker_name = structlog_config.get("WORKER_NAME", False)
        self.unittesting = structlog_config.get("FOR_TESTING", False)
        self.custom_keys = structlog_config.get("CUSTOM_KEYS", {})
        self.sort_keys = structlog_config.get("SORT_KEYS", True)
        self.logger_by_service_name = dict()

    def generate_uuid(self):
        return str(uuid.uuid4())

    def get_dependency(self, worker_ctx):
        service_name = worker_ctx.service_name
        if not self.logger_by_service_name.get(service_name):

            if self.unittesting:
                log_factory = structlog.ReturnLoggerFactory
                chain = [structlog.dev.ConsoleRenderer(colors=False)]
            else:
                log_factory = structlog.stdlib.LoggerFactory

                chain = [
                    structlog.stdlib.filter_by_level,
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.format_exc_info,
                    structlog.processors.UnicodeDecoder(),
                ]
                if self.development_mode:
                    chain.append(structlog.dev.ConsoleRenderer(colors=use_colors))
                else:
                    chain.append(structlog.processors.JSONRenderer(sort_keys=self.sort_keys))

            structlog.configure(
                processors=chain,
                context_class=structlog.threadlocal.wrap_dict(dict),
                logger_factory=log_factory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=True,
            )

            self.logger_by_service_name[service_name] = structlog.get_logger(service_name).new()

        initial_values = {"log_transaction_id": self.generate_uuid(), **self.custom_keys}

        if self.include_worker_name:
            initial_values.update({"entrypoint": worker_ctx.call_id})

        return self.logger_by_service_name[service_name].bind(**initial_values)
