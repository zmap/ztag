from ztag.annotation import * 


class PolyComHTTPS(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        org = d["certificate"]["parsed"]["issuer"]["organization"][0]
        if org == "Polycom, Inc.":
            meta.global_metadata.manufacturer = "Polycom, Inc."
            meta.global_metadata.device_type = Type.CAMERA 
            return meta

