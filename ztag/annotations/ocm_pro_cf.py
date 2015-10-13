from ztag.annotation import *


class OCMProCFMeiAnnotation(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        product_code = obj["mei_response"]["objects"]["product_code"]
        if product_code == "OCM Pro CF":
            meta.global_metadata.manufacturer = Manufacturer.NIVUS
            meta.global_metadata.product = "OCM Pro CF"
            meta.global_metadata.device_type = Type.WATER_FLOW_CONTROLLER
            return meta
