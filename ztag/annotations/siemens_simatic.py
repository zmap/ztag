from ztag.annotation import *


class SiemensSIMATIC(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        product = obj["mei_response"]["objects"]["product_code"].lower()
        if "siemens" in vendor and "simatic" in product:
            meta.global_metadata.manufacturer = Manufacturer.SIEMENS
            meta.global_metadata.product = "SIMATIC"
            return meta
