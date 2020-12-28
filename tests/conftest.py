import pytest
from collections import namedtuple

from nameko.rpc import rpc
from nameko.standalone.rpc import ServiceRpcProxy
from nameko.testing.services import replace_dependencies

from nameko_structlog import StructlogDependency


@pytest.fixture
def service_cls():
    class GreetingService:
        name = "greeting_service"

        log = StructlogDependency()

        @rpc
        def greet(self):
            self.log.info("bar")  # pylint: disable=no-member
            return "Hi"

    return GreetingService


@pytest.fixture
def config(rabbit_config):
    config = rabbit_config.copy()
    config.update({
        "STRUCTLOG": {"INCLUDE_WORKER_NAME": True, "CUSTOM_KEYS": {"action": "testing"}}
    })
    return config


@pytest.fixture
def create_service_meta(container_factory, config, service_cls):
    """ Returns a convenience method for creating service test instance
    `container_factory` is a Nameko's test fixture
    for creating service container
    """
    def create(*dependencies, **dependency_map):
        """ Create service instance with specified dependencies mocked
        Dependencies named in *dependencies will be replaced with a
        `MockDependencyProvider`, which injects a `MagicMock` instead of the
        dependency.
        Alternatively, you may use `dependency_map` keyword arguments
        to name a dependency and provide the replacement value that
        the `MockDependencyProvider` should inject.
        For more information read:
        https://github.com/onefinestay/nameko/blob/master/nameko/testing/services.py#L325
        """
        dependency_names = list(dependencies) + list(dependency_map.keys())

        ServiceMeta = namedtuple(
            "ServiceMeta", ["container"] + dependency_names
        )
        container = container_factory(service_cls, config)

        mocked_dependencies = replace_dependencies(
            container, *dependencies, **dependency_map
        )
        if len(dependency_names) == 1:
            mocked_dependencies = (mocked_dependencies, )

        container.start()

        return ServiceMeta(container, *mocked_dependencies, **dependency_map)

    return create


@pytest.fixture
def greeting_service(create_service_meta):
    """ Greeting service test instance with `log`
    dependency mocked """
    return create_service_meta("log")


@pytest.fixture
def greeting_rpc(config, greeting_service):
    """ Fixture used for triggering real RPC entrypoints on Greeting service """
    with ServiceRpcProxy("greeting_service", config) as proxy:
        yield proxy
