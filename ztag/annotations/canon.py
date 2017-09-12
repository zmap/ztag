from ztag.annotation import *

class CanonHTTPServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if "canon http server" in server.lower():
            meta.global_metadata.manufacturer = Manufacturer.CANON
            meta.global_metadata.device_type = Type.PRINTER
            meta.tags.add("embedded")
            return meta


class CanonHTTPLogo(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
      "canon_lbp6230dn":{
        "global_metadata":{
          "manufacturer":Manufacturer.CANON,
          "device_type":Type.PRINTER,
        },
        "tags":["embedded",]
      }
    }

    def process(self, obj, meta):
        if "/media/canonlogo.gif" in obj["body"]:
            meta.global_metadata.manufacturer = Manufacturer.CANON
            meta.global_metadata.device_type = Type.PRINTER
            meta.tags.add("embedded")
            return meta
