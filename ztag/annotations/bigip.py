from ztag.annotation import *

class BigIPHTTP(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["http_headers"]["server"]

        if "BigIP" in server:
            meta.local_metadata.manufacturer = Manufacturer.BIGIP
            return meta


class BigIPHTTPS(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTP.TLS
    port = None

    def process(self, obj, meta):
        cn = obj["certificate"]["parsed"]["issuer"]["common_name"][0]
        if cn == "bigip":
            meta.local_metadata.manufacturer = Manufacturer.BIGIP
            return meta

