from ztag.annotation import *


class WURMMEIDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "wurm_multigate": {
            "global_metadata": {
                "manufacturer": Manufacturer.WURM,
            }
        }
    }

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"]
        if "wurm" in vendor.lower():
            meta.global_metadata.manufacturer = Manufacturer.WURM
            return meta


class WURMMultigate(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "wurm_multigate": {
            "global_metadata": {
                "manufacturer": Manufacturer.WURM,
                "product": "Multigate",
                "revision": "V1.0",
            }
        }
    }

    def process(self, obj, meta):
        mei_objs = obj["mei_response"]["objects"]
        vendor = mei_objs["vendor"]
        product_code = mei_objs["product_code"]
        if "wurm" not in vendor.lower() or \
                "multigate" not in product_code.lower():
            return
        meta.global_metadata.manufacturer = Manufacturer.WURM
        meta.global_metadata.product = product_code.strip()
        revision = mei_objs.get("revision", "").strip()
        if revision:
            meta.global_metadata.revision = revision
        return meta
