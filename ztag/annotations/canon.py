from ztag.annotation import * 

class CanonHTTPServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):    
        server = obj["headers"]["server"]    
        if "canon http server" in server.lower():
            meta.global_metadata.manufacturer = Manufacturer.Canon
            meta.global_metadata.device_type = Type.PRINTER
            meta.tags.add("embedded")
            return meta
