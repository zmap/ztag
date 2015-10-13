from ztag.annotation import *


class SynchronicMEIDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "synchronic": {
            "global_metadata": {
                "manufacturer": Manufacturer.SYNCHRONIC,
            }
        }
    }

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if "synchronic" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.SYNCHRONIC
            return meta
