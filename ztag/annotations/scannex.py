from ztag.annotation import *

class NetGearSmartSwitch(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "ip.buffer webserver":
            meta.global_metadata.manufacturer = Manufacturer.SCANNEX
            meta.global_metadata.product = "ip.buffer"
            meta.global_metadata.device_type = Type.SCADA_GATEWAY
            meta.tags.add("embedded")
            return meta

