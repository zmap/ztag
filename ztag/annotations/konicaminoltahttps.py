from ztag.annotation import *


class KonicaMinoltaHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
      "konica_minolta_bizhub_c454e":{
        "global_metadata":{
          "manufacturer":Manufacturer.KONICA_MINOLTA,
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        org = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if org == "Konica Minolta":
            meta.global_metadata.manufacturer = Manufacturer.KONICA_MINOLTA


class KonicaMinoltaBizHub(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
      "konica_minolta_bizhub_c454e":{
        "global_metadata":{
          "manufacturer":Manufacturer.KONICA_MINOLTA,
          "product":"Bizhub C454e",
          "device_type":Type.PRINTER
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        org = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if org == "Konica Minolta":
            meta.global_metadata.manufacturer = Manufacturer.KONICA_MINOLTA
        return meta

