from ztag.annotation import *


class LifeSizeHTTPS(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        cn = obj["certificate"]["parsed"]["subject"]["common_name"][0]
        if cn == "LifeSize Transit Server":
            meta.local_metadata.manufacturer = Manufacturer.LIFESIZE
            meta.local_metadata.product = "Transit Server"
            return meta

