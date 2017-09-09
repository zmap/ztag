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
        if obj["title"] == "NETGEAR Web Smart Switch":
            meta.global_metadata.manufacturer = Manufacturer.NETGEAR
            meta.global_metadata.product = "Smart Switch"
            meta.global_metadata.device_type = Type.SWITCH
            meta.tags.add("embedded")
            return meta

