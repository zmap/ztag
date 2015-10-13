from ztag.annotation import * 


class KonicaMinoltaHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        org = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if org == "Konica Minolta":
            meta.global_metadata.manufacturer = Manufacturer.KONICA_MINOLTA
            return meta

