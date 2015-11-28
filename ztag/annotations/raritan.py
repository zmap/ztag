from ztag.annotation import *


class RaritanHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        cn = obj["certificate"]["parsed"]["subject"]["common_name"][0]
        if cn == "Raritan Device":
            meta.global_metadata.manufacturer = Manufacturer.RARITAN
            meta.tags.add("embedded")
            meta.tags.add("data center")
            return meta


