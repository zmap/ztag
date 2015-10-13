from ztag.annotation import *


class VarnishServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        vendor = obj["headers"]["server"]
        if "varnish" in vendor.lower():
            meta.local_metadata.manufacturer = Manufacturer.VARNISH
            meta.local_metadata.product = "HTTP Server"
            return meta
