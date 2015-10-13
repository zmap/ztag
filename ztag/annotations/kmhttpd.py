from ztag.annotation import * 


class KMHttpd(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if "km-httpd" in server.lower():
            meta.local_metadata.product = "KM-httpd"
            if "/" in server:
                meta.local_metadata.version = server.split("/")[1].strip()
            return meta

