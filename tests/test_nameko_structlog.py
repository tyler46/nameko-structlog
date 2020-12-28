#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nameko_structlog` package."""

from unittest.mock import MagicMock, call

from nameko.testing.services import entrypoint_hook
import structlog


class TestingStructlogProcessor:
    """
    Testing StuctlogProcessor that make use of `ReturnLogger`.
    """
    def __init__(self, **kwargs):
        pass

    def get_logger(self):
        structlog.configure(
            processors=[],
            context_class=structlog.threadlocal.wrap_dict(dict),
            logger_factory=structlog.ReturnLoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger().new()


def test_structlog_depedency(greeting_service, greeting_rpc):
    greeting_rpc.log = TestingStructlogProcessor().get_logger()

    with entrypoint_hook(greeting_service.container, "greet") as greet:
        assert greet() == "Hi"

        assert greeting_rpc.log.info("bar") == ((), {"event": "bar"})


def test_strcutlog_logger(greeting_service, greeting_rpc):
    greeting_rpc.log = MagicMock(name="log")
    greeting_rpc.log.info = MagicMock(name="info")
    greeting_rpc.log.info.return_value = TestingStructlogProcessor().get_logger()

    greeting_rpc.log.info("bar")

    assert greeting_rpc.log.info.call_args_list == [call("bar")]
    assert greeting_rpc.log.info.called_once()
