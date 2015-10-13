from ztag.annotation import *


class APCHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        org = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        if "American Power Conversion" in org:
            meta.global_metadata.manufacturer = Manufacturer.APC
            meta.tags.add("embedded")
            return meta
