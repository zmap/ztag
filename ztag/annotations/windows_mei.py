from ztag.annotation import *


class WindowsMEI(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        product_code = obj["mei_response"]["objects"]["product_code"].lower()
        if product_code.startswith("win"):
            meta.global_metadata.os = OperatingSystem.WINDOWS
            return meta

