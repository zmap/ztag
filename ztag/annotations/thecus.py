from ztag.annotation import *

class ThecusNAS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
      "thecus_n7700":{
        "global_metadata":{
          "manufacturer":Manufacturer.THECUS,
          "device_type":Type.NAS,
          "product":"N7700",
        },
        "tags":["embedded"]
      }
    }

    def process(self, obj,meta):
        o = obj["certificate"]["parsed"]["subject"]["organization"][0]
        ou = obj["certificate"]["parsed"]["subject"]["organizational_unit"][0]
        if o == "Thecus Technology Corp.":
            meta.global_metadata.manufacturer = Manufacturer.THECUS
            meta.global_metadata.device_type = Type.NAS
            meta.global_metadata.product = ou
            meta.tags.add("embedded")
            return meta


