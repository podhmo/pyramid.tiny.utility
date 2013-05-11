from pyramid.exceptions import ConfigurationError
from .components import (
    get_interface,
    create_dynamic_interface,
    ConfiguredObject,
    ValidativeObject
)

def maybe_iter(o):
    if hasattr(o, "__iter__"):
        return o
    return [o]

def as_interfaces(src):
    return tuple([create_dynamic_interface(c.__name__) 
                  for c in maybe_iter(src)])

## directive

def add_instance(config, provided, name=""):
    interface = get_interface(provided)
    if interface is None:
        raise ConfigurationError("{0} is not have _interface".format(provided)
) 
    if hasattr(provided, "validate"):
        provided.validate()
    def register():
        config.registry.registerUtility(provided, interface, name=name)
    config.action("tinyUtility", register)

def add_instance_from_settings(config, cls, settings, name=""):
    provided = cls.from_settings(settings)
    add_instance(config, provided, name=name)

def add_mapping(config, src, dst, value=None, name=""):
    isrc = as_interfaces(src)
    idst = create_dynamic_interface(dst.__name__)
    value = value or dst
    def register():
        config.registry.adapters.register(isrc, idst, name=name, value=value)
    config.action("tinyAdapter", register)

## create

def create_configured_instance_lookup(tiny_utility_cls, name=None):
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
    config.add_directive("add_instance", add_instance)
    config.add_directive("add_instance_from_settings", add_instance_from_settings)
    config.add_directive("add_mapping", add_mapping)
