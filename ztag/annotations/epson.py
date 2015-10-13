from ztag.annotation import *


class EpsonServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["headers"]["server"]    
        if "epson_linux" in server.lower():
            meta.global_metadata.manufacturer = Manufacturer.EPSON 
            return meta
