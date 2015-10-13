from ztag.annotation import * 


class EMCHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        organizational_unit = obj["certificate"]["parsed"]["issuer"]["organizational_unit"][0]
        if "EMC" in organization and "CLARiiON" in organizational_unit:
            meta.global_metadata.manufacturer = "EMC"
            meta.device_type = Type.NAS
            return meta

