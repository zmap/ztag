from ztag.annotation import Annotation, Manufacturer

from ztag import protocols


class INTEGDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    vals = {
        "manufacturer": Manufacturer.INTEG,
    }

    def _process(self, d):
        vendor = d["mei_response"]["objects"]["vendor"].lower()
        if "integ" in vendor:
            return ([], self.vals)
