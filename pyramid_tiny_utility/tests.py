from pyramid import testing
import pytest

_config = None
def setup_function(fn):
    global _config
    _config = testing.setUp()
    _config.include("pyramid_tiny_utility")

def teardown_function(fn):
    global _config
    _config = None
    testing.tearDown()

def _create_utility():
    from pyramid_tiny_utility import ConfiguredObject
    class U(ConfiguredObject):
        pass
    return U

## test
def test_add_directive():
    assert _config.add_instance

def test_tiny_utility_has_interface():
    from pyramid_tiny_utility import get_interface
    from zope.interface.interface import InterfaceClass

    u = _create_utility()()
    interface = get_interface(u)
    assert isinstance(interface, InterfaceClass)

def test_register_utility():
    from pyramid_tiny_utility import get_interface
    u = _create_utility()()
    _config.add_instance(u)

    interface = get_interface(u)
    assert u == _config.registry.queryUtility(interface)
    
def test_lookup_factory():
    from pyramid_tiny_utility import create_configured_instance_lookup
    u = _create_utility()()
    _config.add_instance(u)

    lookup = create_configured_instance_lookup(u)
    class request:
        registry = _config.registry

    assert u == lookup(request)

def test_multi_lookup_by_name():
    from pyramid_tiny_utility import create_configured_instance_lookup
    u0 = _create_utility()()
    u1 = _create_utility()()

    _config.add_instance(u0)
    _config.add_instance(u1,name="another")

    lookup = create_configured_instance_lookup(u0)
    class request:
        registry = _config.registry

    assert u0 == lookup(request)
    assert u1 == lookup(request, name="another")

def test_many_kinds_utility():
    from pyramid_tiny_utility import ConfiguredObject
    from pyramid_tiny_utility import create_configured_instance_lookup        
    class A(ConfiguredObject):
        pass
    class B(ConfiguredObject):
        pass

    lookupA = create_configured_instance_lookup(A)
    lookupB = create_configured_instance_lookup(B)

    a = A()
    b = B()
    _config.add_instance(a)
    _config.add_instance(b)
    
    class request:
        registry = _config.registry

    assert a == lookupA(request)
    assert b == lookupB(request)
    

def test_register_utility_after_set_validation():
    from pyramid_tiny_utility.components import ConfiguredObject
    from pyramid.exceptions import ConfigurationError

    class HasValidation(ConfiguredObject):
        def __init__(self, depends=None):
            self.depends = depends

        from_settings = ConfiguredObject.create_from_settings_from_paramters(["depends"], prefix="test.")

    def assert_depends(o):
        if not o.depends:
            raise ConfigurationError("")
    _config.add_validation(HasValidation, assert_depends)

    settings = {"test.depends": True}
    _config.add_instance_from_settings(HasValidation, settings)

    settings = {"test.depends": False}
    with pytest.raises(ConfigurationError):
        _config.add_instance_from_settings(HasValidation, settings)

def test_register_utility_before_set_validation():
    from pyramid_tiny_utility.components import ConfiguredObject
    from pyramid.exceptions import ConfigurationError

    class HasValidation(ConfiguredObject):
        pass

    def always_error(o):
        raise ConfigurationError("")

    _config.add_validation(HasValidation, always_error)

    with pytest.raises(ConfigurationError):
        _config.add_instance(HasValidation())

## mapping
def test_mapping():
    from pyramid_tiny_utility import get_mapping_from_class
    # src -> container
    class Container(object):
        def __init__(self, src):
            self.src = src

    class Source(object):
        pass

    _config.add_mapping(Source, Container)
    
    class request:
        registry = _config.registry
    mapping = get_mapping_from_class(request, Source, Container)

    src = Source()
    mapped = mapping(src)
    assert isinstance(mapped, Container)

def test_mapping_another():
    from pyramid_tiny_utility import get_mapping_from_class
    class A():
        pass

    class Adapter(object):
        def __init__(self, a):
            self.a = a

    class BAdapter(Adapter):
        pass
    class CAdapter(Adapter):
        pass

    _config.add_mapping(A, Adapter, BAdapter)
    _config.add_mapping(A, Adapter, CAdapter, name="c-case")
    
    class request:
        registry = _config.registry

    mapping = get_mapping_from_class(request, A, Adapter)
    a = A()
    mapped = mapping(a)
    assert isinstance(mapped, BAdapter)

    mapping = get_mapping_from_class(request, A, Adapter, name="c-case")
    a = A()
    mapped = mapping(a)
    assert isinstance(mapped, CAdapter)
