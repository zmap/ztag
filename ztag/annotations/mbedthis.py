from ztag.annotation import *


class MbedthisAppweb(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if "mbedthis-appweb" in server.lower():
            meta.local_metadata.product = "Mbedthis-Appweb"
            if "/" in server:
                meta.local_metadata.version = server.split("/")[1].strip()
            return meta

