from ztag.annotation import *


class LexmarkHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if organization == "Lexmark":
            meta.global_metadata.manufacturer = Manufacturer.LEXMARK
            cn = obj["certificate"]["parsed"]["issuer"]["common_name"][0]
            if cn == "Lexmark Laser Printer": 
                meta.global_metadata.device_type = Type.LASER_PRINTER
            else:
                meta.global_metadata.product = cn.split(" ", 1)[1]
                meta.global_metadata.device_type = Type.PRINTER
            return meta

