from ztag.annotation import *

class AppleServerHTTP(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "macOS Server":
            meta.global_metadata.manufacturer = Manufacturer.APPLE
            return meta
