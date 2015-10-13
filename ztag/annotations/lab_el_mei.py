from ztag.annotation import * 


class LABELAnnotation(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = obj["mei"]["objects"]["vendor"].lower()
        if "lab-el" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.LAB_EL
