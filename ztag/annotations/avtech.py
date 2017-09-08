from ztag.annotation import *

class AVTECH(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "avtech_room_alert_32ew":{
        "global_metadata":{
          "manufacturer":Manufacturer.AVTECH,
          "device_type":Type.ENVIRONMENT_MONITOR,
          "product":"Room Alert 32E/W",
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        if obj["title"].startswith("AVTECH Software, Inc."):
            meta.global_metadata.manufacturer = Manufacturer.AVTECH
            meta.global_metadata.device_type = Type.ENVIRONMENT_MONITOR
            meta.tags.add("embedded")
            if "-" in obj["title"]:
                _, product, _ = obj["title"].split("-")
                product = product.strip()
                product = product.replace("&reg;", "")
                meta.global_metadata.product = product
            return meta

