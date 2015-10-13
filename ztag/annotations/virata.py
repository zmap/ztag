from ztag.annotation import *

class VirataServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):  
        server = obj["headers"]["server"]
        if "virata-emweb" in server.lower():
            meta.global_metadata.manufacturer = Manufacturer.VIRATA
            meta.global_metadata.product = "EmWeb"
            if "/" in server:
                meta.global_metadata.version = server.split("/")[-1]
            return meta

