#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nameko_structlog` package."""


import pytest

from nameko.rpc import rpc
from nameko.testing.services import (
    entrypoint_hook, entrypoint_waiter, get_extension,
)

from nameko_structlog import StructlogDependency


@pytest.fixture
def config():

    return {
        'STRUCTLOG': {
            'FOR_TESTING': True
        }
    }


@pytest.fixture
def service_cls():

    class Service(object):
        name = 'demo'

        log = StructlogDependency()

        @rpc
        def foo(self):
            self.log.info('bar')  # pylint: disable=no-member
            return 'OK'

    return Service


def test_structlog_setup(container_factory, service_cls, config):
    container = container_factory(service_cls, config)
    container.start()

    struct_log = get_extension(container, StructlogDependency)

    with entrypoint_hook(container, 'foo') as foo:
        with entrypoint_waiter(container, 'foo'):
            assert foo() == 'OK'
            # StructlogDependency returns a structlog logger per service name
            service_logger = struct_log.logger_by_service_name['demo']
            assert 'bar' == service_logger.info('bar')
