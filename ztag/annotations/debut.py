from ztag.annotation import *

class Debut(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, d):  
        s = d["headers"]["server"]
        if "debut" in s:
            meta.local_metadata.product = "debut"
            if "/" in s:
                meta.local_metadata.version = s.split("/", 1)[1]
        return meta

