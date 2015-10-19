import os
import os.path
import json

class Device(object):

    _devices_by_name = {}

    @classmethod
    def _populate_devices(cls):
        path = os.path.join(os.path.dirname(__file__), "devices")
        for file in os.listdir(path):
            if file.startswith("."):
                continue
            full_path = os.path.join(path, file)
            assert os.path.exists(full_path)
            name = ".".join(file.split(".")[:-1])
            content = open(full_path).read()
            try:
                cls._devices_by_name[name] = cls(content)
            except:
                raise Exception("Device %s is not a valid JSON document" % name)

    @classmethod
    def from_name(cls, name):
        if not cls._devices_by_name:
            cls._populate_devices()
        if name not in cls._devices_by_name:
            raise Exception("Specified device %s does not exist." % name)
        return cls._devices_by_name[name]

    def __init__(self, doc):
        self.source = json.loads(doc)
    
    def get(self, port, protocol, subprotocol):
        if port:
            return self.source[str(port)][protocol.pretty_name][subprotocol.pretty_name]
        else:
            for port in self.source.keys():
                if type(self.source[port]) == dict and protocol.pretty_name in self.source[port]:
                    return self.source[port][protocol.pretty_name][subprotocol.pretty_name]



Device._populate_devices()
