from ztag.annotation import * 


class HPPrinterHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj,meta):
        cn = obj["certificate"]["parsed"]["issuer"]["common_name"][0]
        if "HP-Printers" in cn:
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.global_metadata.device_type = Type.PRINTER
            return meta

