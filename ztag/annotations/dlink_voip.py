from ztag.annotation import *

class DLinkVoIPRouter(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"].strip() == "D-Link VoIP Router":
            meta.global_metadata.manufacturer = Manufacturer.DLINK
            meta.global_metadata.product = "VoIP Router"
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.tags.add("embedded")
            return meta


class DLinkWirelessRouter(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"].strip() == "D-LINK SYSTEMS, INC. | WIRELESS ROUTER":
            meta.global_metadata.manufacturer = Manufacturer.DLINK
            meta.global_metadata.product = "Wireless Router"
            meta.global_metadata.device_type = Type.SOHO_ROUTER
            meta.tags.add("embedded")
            return meta

