from ztag.annotation import *

class ArubaHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = meta["certificate"]["parsed"]["subject"]["organization"][0]

        if organization == "Aruba Networks":
            meta.global_metadata.manufacturer = Manufacturer.ARUBA
            meta.global_metadata.device_type = Type.WIFI
            meta.tags.add("embedded")
            return meta
