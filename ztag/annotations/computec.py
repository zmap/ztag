from ztag.annotation import *


class ComputecOYMEIDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "computec": {
            "global_metadata": {
                "manufacturer": Manufacturer.COMPUTEC,
            }
        }
    }

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if "computec oy" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.COMPUTEC
            return meta


class ComputecController(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "computec_cws": {
            "global_metadata": {
                "manufacturer": Manufacturer.COMPUTEC,
                "product": "CWS06",
                "revision": "v3.159",
                "device_type": Type.SCADA_CONTROLLER,
            }
        }
    }

    def process(self, obj, meta):
        mei_objs = obj["mei_response"]["objects"]
        vendor = mei_objs["vendor"]
        product_code = mei_objs["product_code"]
        if "computec oy" not in vendor.lower():
            return
        if "cws" not in product_code.lower():
            return
        meta.global_metadata.manufacturer = Manufacturer.COMPUTEC
        meta.global_metadata.product = product_code.rstrip()
        meta.global_metadata.revision = mei_objs.get("revision", None)
        meta.global_metadata.device_type = Type.SCADA_CONTROLLER
        return meta
