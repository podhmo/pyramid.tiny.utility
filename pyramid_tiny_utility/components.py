from zope.interface import Interface
from zope.interface import implementer
from pyramid.exceptions import ConfigurationError
from functools import partial

def check_reserved_word(candidates, name, exclass=ConfigurationError):
    if name in candidates:
        raise exclass("{0} is reserved name".format(name))

def get_interface(tiny_utility_cls):
    return getattr(tiny_utility_cls,"_interface")

_cache = {}
def _create_dynamic_interface(name=None, cache=None):
    if not name in cache:
        cache[name] = Interface.__class__(name=name)
    return cache[name]
create_dynamic_interface = partial(_create_dynamic_interface, cache=_cache)

## utility
class ConfiguredObjectMeta(type):
    def __new__(cls, name, base, attrs):
        check_reserved_word(attrs, "_interface")
        attrs["_interface"] = iface = create_dynamic_interface("I"+name)
        return implementer(iface)(type(name, base, attrs))

class ConfiguredObject(object):
    __metaclass__ = ConfiguredObjectMeta

    @classmethod
    def from_settings(cls, settings):
        return cls()

    @classmethod
    def create_from_settings_from_paramters(cls, ks, prefix=""):
        @classmethod
        def from_settings(cls, settings):
            params = {k:settings.get(prefix+k) for k in ks}
            return cls(**params)
        return from_settings

def classname(cls):
    if hasattr(cls, "__classname__"):
        return cls.__classname__
    return cls.__name__
