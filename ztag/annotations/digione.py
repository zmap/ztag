from ztag.annotation import *

class DigiOne(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "digi_one":{
        "global_metadata":{
          "manufacturer":Manufacturer.DIGI,
          "device_type":Type.SCADA_GATEWAY,
          "product":"One",
        },
        "tags":["embedded","scada"]
      }
    }


    def process(self, obj, meta):
        if obj["title"].strip() == "Digi One SP&nbsp;Configuration and Management":
            meta.global_metadata.manufacturer = Manufacturer.DIGI
            meta.global_metadata.product = "One"
            meta.global_metadata.device_type = Type.SCADA_GATEWAY
            meta.tags.add("embedded")
            meta.tags.add("scada")
            return meta

