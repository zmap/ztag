from ztag.annotation import *

class JetDirectHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        org = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        cn = obj["certificate"]["parsed"]["issuer"]["common_name"][0]

        if "HP Jetdirect" in cn and "Hewlett-Packard" in org:
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.product = "JetDirect" 
            meta.global_metadata.device_type = Type.PRINTER
            return meta
        elif "HP Designjet" in cn and "Hewlett-Packard" in org:
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.product = "DesignJet" 
            meta.global_metadata.device_type = Type.PRINTER
            return meta

