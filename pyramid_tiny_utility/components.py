from zope.interface import Interface
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
class TinyUtilityMeta(type):
    def __new__(cls, name, base, attrs):
        check_reserved_word(attrs, "_interface")
        attrs["_interface"] = provided = create_dynamic_interface("I"+name)
        return type(name, base, attrs)

class TinyUtility(object):
    __metaclass__ = TinyUtilityMeta

    @classmethod
    def from_settings(cls, settings):
        return cls()

    @classmethod
    def create_from_settings_from_paramters(cls, ks):
        @classmethod
        def from_settings(cls, settings):
            params = {k:settings.get(k) for k in ks}
            return cls(**params)
        return from_settings

class ValidativeUtility(TinyUtility):
    def validate(self):
        raise NotImplementedError

def classname(cls):
    if hasattr(cls, "__classname__"):
        return cls.__classname__
    return cls.__name__
