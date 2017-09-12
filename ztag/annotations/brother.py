from ztag.annotation import *

class BrotherPrinter(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "brother_mfc_8950dtw":{
        "global_metadata":{
          "manufacturer":Manufacturer.BROTHER,
          "device_type":Type.PRINTER,
          "product":"MFC-8950DW",
        },
        "tags":["embedded",]
      },
      "brother_hl_6180dw":{
        "global_metadata":{
          "manufacturer":Manufacturer.BROTHER,
          "device_type":Type.PRINTER,
          "product":"HL-6180DW",
        },
        "tags":["embedded",]
      }

    }

    def process(self, obj, meta):
        title = obj["title"].strip()
        if title.startswith("Brother "):
            meta.global_metadata.manufacturer = Manufacturer.BROTHER
            meta.global_metadata.device_type = Type.PRINTER
            product = title.split(" ", 1)[1]
            product = product.replace("series", "")
            product = product.strip()
            meta.global_metadata.product = product
            meta.tags.add("embedded")
            return meta
