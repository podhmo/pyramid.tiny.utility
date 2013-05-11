from pyramid.exceptions import ConfigurationError
from .components import (
    get_interface,
    TinyUtility,
    ValidativeUtility
)

## directive
def register_tiny_utility(config, provided, name=""):
    interface = get_interface(provided)
    if interface is None:
        raise ConfigurationError("{0} is not have _interface".format(provided))
    config.registry.registerUtility(provided, interface, name=name)

def register_tiny_utility_from_settings(config, cls, settings, name=""):
    provided = cls.from_settings(settings)
    if hasattr(provided, "validate"):
        provided.validate()
    register_tiny_utility(config, provided, name=name)

def create_lookup_function(tiny_utility_cls, name=None):
    interface = get_interface(tiny_utility_cls)
    def _lookup(request,name=""):
        return request.registry.queryUtility(interface,name=name)
    if name:
        _lookup.__name__ = name
    return _lookup

def includeme(config):
    config.add_directive("register_tiny_utility", register_tiny_utility)
    config.add_directive("register_tiny_utility_from_settings", register_tiny_utility_from_settings)
