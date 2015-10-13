from ztag.annotation import * 


class SharpHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        common_name = obj["certificate"]["parsed"]["issuer"]["common_name"][0]
        if "Sharp Corporation" in organization:
            meta.global_metadata.manufacturer = Manufacturer.SHARP
            if "MX-B401" in common_name:
                meta.global_metadata.product = "MX-B401" 
                meta.global_metadata.device_type = Type.PRINTER
            return meta


