from ztag.annotation import *

class BomgarServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    # http://www.bomgar.com/

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if server == "Bomgar":
            meta.local_metadata.manufacturer = "Bomgar"
            meta.tags.add("remote access")
            return meta
