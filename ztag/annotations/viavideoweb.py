from ztag.annotation import *


class ViaVideoWeb(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):    
        server = obj["headers"]["server"]    
        if "viavideo" in server.lower():
            meta.global_metadata.manufacturer = Manufacturer.VIA
            return meta
