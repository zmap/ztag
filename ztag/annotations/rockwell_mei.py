from ztag.annotation import *


class RockwellAutomationAnnotation(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if "rockwell automation" in vendor or "allen-bradley" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.ROCKWELL
            return meta


class RockwellAutomation141(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    MODELS = {
        "141"
    }

    tests = {
        "rockwell_141": {
            "global_metadata": {
                "manufacturer": Manufacturer.ROCKWELL,
                "product": "141",
                "revision": "08.0B",
            }
        }
    }

    def process(self, obj, meta):
        mei_objs = obj["mei_response"]["objects"]
        vendor = mei_objs["vendor"]
        product_code = mei_objs["product_code"]
        if "rockwell automation" not in vendor.lower():
            return
        if "141" not in product_code.lower():
            return
        meta.global_metadata.manufacturer = Manufacturer.ROCKWELL
        meta.global_metadata.product = product_code.strip()
        revision = mei_objs.get("revision", "").strip()
        if revision:
            meta.global_metadata.revision = revision
        return meta
