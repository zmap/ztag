from ztag.annotation import *

class MikroTikHTTP(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "mikrotik routeros > administration" or \
                obj["title"] == "RouterOS router configuration page":
            meta.global_metadata.manufacturer = Manufacturer.MIKROTIK
            meta.global_metadata.os = OperatingSystem.MIKROTIK_ROUTER_OS
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta



