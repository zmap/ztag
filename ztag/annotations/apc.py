from ztag.annotation import *


class APCHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        org = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if "American Power Conversion" in org:
            meta.global_metadata.manufacturer = Manufacturer.APC
            meta.tags.add("embedded")
            return meta


class APCApplicationError(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "apc_application_error":{
        "global_metadata":{
          "manufacturer":Manufacturer.APC
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        if obj["title"] == "APC | Application Error":
            meta.global_metadata.manufacturer = Manufacturer.APC
            meta.tags.add("embedded")
            return meta


