from ztag.annotation import *

class TPLinkTLWR1043ND(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "TL-WR1043ND":
            meta.global_metadata.manufacturer = Manufacturer.TPLINK
            meta.global_metadata.product = "TL-WR1043ND Wireless N Gigabit Router "
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.tags.add("embedded")
            return meta

