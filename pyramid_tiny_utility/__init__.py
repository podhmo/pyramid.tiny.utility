from pyramid.exceptions import ConfigurationError
from .components import (
    get_interface,
    create_dynamic_interface,
    TinyUtility,
    ValidativeUtility
)

def maybe_iter(o):
    if hasattr(o, "__iter__"):
        return o
    return [o]

def as_interfaces(src):
    return tuple([create_dynamic_interface(c.__name__) 
                  for c in maybe_iter(src)])

## directive

def register_tiny_utility(config, provided, name=""):
    interface = get_interface(provided)
    if interface is None:
        raise ConfigurationError("{0} is not have _interface".format(provided)
) 
    if hasattr(provided, "validate"):
        provided.validate()
    config.registry.registerUtility(provided, interface, name=name)

def register_tiny_utility_from_settings(config, cls, settings, name=""):
    provided = cls.from_settings(settings)
    register_tiny_utility(config, provided, name=name)

def register_mapping(config, src, dst, value=None, name=""):
    isrc = as_interfaces(src)
    idst = create_dynamic_interface(dst.__name__)
    value = value or dst
    config.registry.adapters.register(isrc, idst, name=name, value=value)

## create

def create_lookup(tiny_utility_cls, name=None):
    interface = get_interface(tiny_utility_cls)
    def _lookup(request,name=""):
        return request.registry.queryUtility(interface,name=name)
    if name:
        _lookup.__name__ = name
    return _lookup

def get_mapping_from_class(request, src, dst, name=""):
    isrc = as_interfaces(src)
    idst = create_dynamic_interface(dst.__name__)
    def mapping(*args):
        return request.registry.adapters.lookup(isrc, idst, name=name)(*args)
    return mapping

def get_mapping(request, src, dst, name=""):
    return get_mapping_from_class(request, src.__class__, dst, name=name)

def includeme(config):
    config.add_directive("register_tiny_utility", register_tiny_utility)
    config.add_directive("register_tiny_utility_from_settings", register_tiny_utility_from_settings)
    config.add_directive("register_mapping", register_mapping)
