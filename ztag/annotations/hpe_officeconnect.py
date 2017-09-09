from ztag.annotation import *

class HPOfficeConnectSwitch(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "hpe_officeconnect_switch_1820":{
        "global_metadata":{
          "manufacturer":Manufacturer.HP,
          "device_type":Type.SWITCH,
          "product":"OfficeConnect Switch 1820",
          "version":"48G J9981A",
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

