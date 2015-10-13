from ztag.annotation import *

class BoaServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if server[:3] == "Boa":
            meta.local_metadata.product, meta.local_metadata.version = \
                    server.split("/")
            return meta
