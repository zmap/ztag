from ztag.annotation import *


class LiteSpeed(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if "litespeed" in server:
            meta.local_metadata.product = "LiteSpeed"
            return meta
