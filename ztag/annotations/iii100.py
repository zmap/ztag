from ztag.annotation import *


class III100Server(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["headers"]["server"]

        if "iii 100" in server.lower():
            meta.local_metadata.product = "III 100"
            return meta

