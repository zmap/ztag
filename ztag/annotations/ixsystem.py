from ztag.annotation import * 


class IXsystemHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        org = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if "iXsystems" in org:
            meta.global_metadata.manufacturer = Manufacturer.IXSYSTEMS
            meta.global_metadata.device_type = Type.NAS 
            return meta

