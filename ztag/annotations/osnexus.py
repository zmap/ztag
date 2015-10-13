from ztag.annotation import * 


class OSNEXUS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        cn = d["certificate"]["parsed"]["issuer"]["common_name"][0]
        if cn == "OSNEXUS":
            meta.global_metadata.manufacturer = "OS NEXUS"
            meta.global_metadata.product = "Quantator"
            meta.global_metadata.device_type = Type.STORAGE
            return meta


