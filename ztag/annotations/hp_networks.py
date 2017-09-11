from ztag.annotation import *

class HPNetworksWebInterface(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "hp_networks":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.NETWORK,
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        if obj["title"] == "HP Networks Web Interface":
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta

