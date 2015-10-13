from ztag.annotation import *


class MicrosoftIIS(Annotation):

    name = "Microsoft IIS"

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = d["headers"]["server"]  
        if "microsoft-iis" in server:
            meta.local_metadata.manufacturer = Manufacturer.MICROSOFT
            meta.local_metadata.product = "IIS" 
            if "/" in server:
                meta.local_metadata.version = server.split("/")[1].strip()
            return meta

