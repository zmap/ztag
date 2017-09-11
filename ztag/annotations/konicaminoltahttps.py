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
        org = obj["certificate"]["parsed"]["issuer"]["organization"][0].lower()
        if org == "konica minolta":
            meta.global_metadata.manufacturer = Manufacturer.KONICA_MINOLTA
            meta.tags.add("embedded")
            return meta


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
        org = obj["certificate"]["parsed"]["issuer"]["organization"][0].lower()
        if org == "konica minolta":
            meta.global_metadata.manufacturer = Manufacturer.KONICA_MINOLTA
            for ou in obj["certificate"]["parsed"]["subject"]["organizational_unit"]:
                if "bizhub" in ou:
                    ou = ou.replace("KONICA MINOLTA", "").replace("bizhub", "").strip()
                    if ou:
                        product = " ".join(["Bizhub", ou])
                        meta.global_metadata.product = product
                    else:
                        meta.global_metadata.product = "Bizhub"
                    meta.global_metadata.device_type = Type.PRINTER
                    meta.tags.add("embedded")
                    return meta

