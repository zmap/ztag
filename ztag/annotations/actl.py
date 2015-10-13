from ztag.annotation import *


class ACTLDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "actl": {
            "global_metadata": {
                "manufacturer": Manufacturer.ACTL,
            }
        }
    }

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if "actl" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.ACTL
            return meta
