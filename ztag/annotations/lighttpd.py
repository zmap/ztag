from ztag.annotation import *


class Lighttpd(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if "lighttpd" in server:
            meta.local_metadata.product = "lighttpd"
            if "/" in server:
                meta.local_metadata.version = server.split("/")[1].strip()
            return meta

