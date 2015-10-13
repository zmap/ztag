from ztag.annotation import *

class GoAheadWebs(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):    
        server = obj["headers"]["server"]    
        if "goahead-webs" in server.lower():
            meta.local_metadata.product = "GoAhead-Webs"
            return meta
