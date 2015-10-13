from ztag.annotation import *


class WegMEIAnnotation(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if vendor == "weg":
            meta.global_metadata.manufacturer = Manufacturer.WEG
            return meta

