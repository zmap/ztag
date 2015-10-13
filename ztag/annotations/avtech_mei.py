from ztag.annotation import * 


class AVTECHDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = d["mei_response"]["objects"]["vendor"].lower()
        if "avtech" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.AVTECH
            meta.tags.add("scada")
