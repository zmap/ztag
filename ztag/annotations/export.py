from ztag.annotation import *


class RSAExportTag(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.RSA_EXPORT
    port = None

    def process(self, obj, meta):
        if obj["support"]:
            meta.tags.add("rsa-export")
            return meta


class DHEExportTag(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.DHE_EXPORT
    port = None

    def process(self, obj, meta):
        if obj["support"]:
            meta.tags.add("dhe-export")
            return meta
