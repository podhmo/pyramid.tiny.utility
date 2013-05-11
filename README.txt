```
### Utility
from pyramid import testing
from pyramid_tiny_utility import ConfiguredObject, create_configured_instance_lookup

class Uploader(ConfiguredObject):
    def __init__(self, storepath):
        self.storepath = storepath

get_uploder = create_configured_instance_lookup(Uploader)
    
settings = {
    "demo.uploader.storepath": "/tmp/storepath"
}

config = testing.setUp()
config.include("pyramid_tiny_utility")
config.add_instance(Uploader(settings["demo.uploader.storepath"]))

## request
class request:
    registry = config.registry
uploader = get_uploder(request)
assert uploader.storepath == "/tmp/storepath"

testing.tearDown()
```

```
### Valiadative Utility

## request

class request:
    registry = config.registry

mail_management = get_mailmanagemt(request)

assert mail_management.sender == "foo@bar.jp"
assert mail_management.default_title == "default"

testing.tearDown()
```

```
### Adapter
class Model(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class Render:
    pass

class RowRender(object):
    def __init__(self, o):
        self.o = o

    def render(self):
        r = ["<tr>"]
        r.append("<td>{0}</td>".format(self.o.x))
        r.append("<td>{0}</td>".format(self.o.y))
        r.append("<td>{0}</td>".format(self.o.z))
        r.append("</tr>")
        return "".join(r)
    
class ListRender(object):
    def __init__(self, o):
        self.o = o

    def render(self):
        r = ["<ul>"]
        r.append("<li>{0}</li>".format(self.o.x))
        r.append("<li>{0}</li>".format(self.o.y))
        r.append("<li>{0}</li>".format(self.o.z))
        r.append("</ul>")
        return "".join(r)

## configuration

config = testing.setUp()
config.include("pyramid_tiny_utility")
config.add_mapping(Model, Render, RowRender)
config.add_mapping(Model, Render, RowRender, name="row")
config.add_mapping(Model, Render, ListRender, name="list")


## request
class request:
    registry = config.registry

from pyramid_tiny_utility import get_mapping

model = Model(10,20,30)
print get_mapping(request, model, Render)(model).render()
print get_mapping(request, model, Render, name="list")(model).render()
```
