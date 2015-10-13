from ztag.annotation import *


class PoKeys56E(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        product_code = obj["mei_response"]["objects"]["product_code"].lower()
        if 'pokeys56e' in product_code:
            meta.global_metadata.manufacturer = Manufacturer.POLABS
            meta.global_metadata.product = "PoKeys56E" 
            meta.global_metadata.device_type = Type.SCADA_GATEWAY

