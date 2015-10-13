from ztag.annotation import *

class HPIRGHTTPS(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        ou = obj["certificate"]["parsed"]["issuer"]["organizational_unit"][0]
        if "HP-IPG" in ou:
            meta.global_metadata.manufacturer = Manufacturer.HP
            meta.local_metadata.product = "HP IRG"
            return meta
