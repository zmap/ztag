from ztag.annotation import *

class Comtrol(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if "comtrol" in organization.lower():
            meta.local_metadata.manufacturer = Manufacturer.COMTROL 
            return meta

