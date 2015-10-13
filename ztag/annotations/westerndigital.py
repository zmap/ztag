from ztag.annotation import *


class WesternDigital(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        ou = obj["certificate"]["parsed"]["issuer"]["organizational_unit"][0]
        if "Western Digital" in organization and "Branded Products" in ou:
            meta.global_metadata.manufacturer = Manufacturer.Western_Digital
            return meta


