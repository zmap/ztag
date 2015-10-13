from ztag.annotation import *


class VerisE51C3(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        product = obj["mei_response"]["objects"]["product_code"].lower()
        if "veris" in vendor and "e51c3" in product:
            meta.global_metadata.manufacturer = Manufacturer.VERIS
            meta.global_metadata.product = "E51C3"
            meta.global_metadata.device_type = Type.POWER_MONITOR
            return meta
