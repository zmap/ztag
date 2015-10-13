from ztag.annotation import Annotation, TLSTag


from ztag import protocols
import ztag.test


class XeroxHTTPS(TLSTag):

    name = "XEROX HTTPS"

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = obj["certificate"]["certificate"]["issuer"]["organization"]
        if "Xerox Corporation" in organization: 
            meta.local_metadata.manufacturer = Manufacturer.XEROX
            meta.local_metadata.product = "HTTPS Server"
            meta.local_metadata.device = "XEROX HTTPS Server"
            meta.local_metadata.type = TYPE_XEROX_DEVICE
            return meta
        return None 

