from ztag.annotation import *


class SolarLogMEIAnnotation(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if "solare" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.SOLAR_LOG
            meta.global_metadata.device_type = Type.SOLAR_PANEL
            return meta
