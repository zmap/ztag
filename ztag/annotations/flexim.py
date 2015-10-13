from ztag.annotation import *


class FleximMEIDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "flexim": {
            "global_metadata": {
                "manufacturer": Manufacturer.FLEXIM,
            }
        }
    }

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"]
        if "flexim" in vendor.lower():
            meta.global_metadata.manufacturer = Manufacturer.FLEXIM
            return meta
