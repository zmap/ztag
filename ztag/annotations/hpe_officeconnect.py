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
        if obj["title"].startswith("HPE OfficeConnect Switch"):
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.product = "OfficeConnect Switch"
            meta.global_metadata.device_type = Type.SWITCH
            # try to parse out version if available
            if len(obj["title"]) > 25:
                remainder = str(obj["title"][25:])
                if " " in remainder:
                    product, version = remainder.split(" ", 1)
                    meta.global_metadata.product += " "
                    meta.global_metadata.product += product
                    meta.global_metadata.version = version
                else:
                    meta.global_metadata.product += " "
                    meta.global_metadata.product += remainder
            meta.tags.add("embedded")
            return meta

