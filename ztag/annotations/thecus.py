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
          "product":"n7700",
        },
        "tags":["embedded"]
      }
    }

    def process(self, obj,meta):
        ou = obj["certificate"]["parsed"]["issuer"]["organizational_unit"][0]
        if ou == "OpenCMC Group":
            meta.global_metadata.manufacturer = Manufacturer.DELL
            meta.global_metadata.device_type = Type.SERVER_MANAGEMENT
            meta.tags.add("embedded")
            return meta


