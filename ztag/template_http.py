from ztag.annotation import *

class NetGearSmartSwitch(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "netgear_smart_switch":{
        "global_metadata":{
          "manufacturer":Manufacturer.NETGEAR,
          "device_type":Type.SWITCH,
          "product":"Smart Switch",
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

