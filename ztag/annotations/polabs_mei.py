from ztag.annotation import *


class PoLabsDeviceAnnotation(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if 'polabs' in vendor:
            meta.global_metadata.manufacturer = Manufacturer.POLABS
