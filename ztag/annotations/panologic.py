from ztag.annotation import *


class PanoLogicHTTPS(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        org = d["certificate"]["parsed"]["issuer"]["organization"][0]
        if org == "Pano Logic, Inc.":
            meta.local_metadata.manufacturer = org
            meta.tags.add("thin client")
            meta.tags.add("remote access")
            return meta
