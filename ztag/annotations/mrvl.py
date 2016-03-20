from ztag.annotation import *


class MRV1Server(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        s = obj["headers"]["server"]
        if s.startswith("Mrvl"):
            meta.local_metadata.product = "Mrvl"
            v = s.split("-")[1].replace("_", ".")
            meta.local_metadata.version = v
            return meta
