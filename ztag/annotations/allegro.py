from ztag.annotation import *

class HttpAllegroServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):	
        server = obj["headers"]["server"]
        if "allegro" in server.lower():
            meta.local_metadata.manufacturer = Manufacturer.ALLEGRO
            meta.local_metadata.product = "RomPager"
            if "/" in server:
                meta.local_metadata.version  = server.split("/", 1)[1]
            return meta

