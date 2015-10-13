from ztag.annotation import *


class CrouzetMEIDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "crouzet": {
            "global_metadata": {
                "manufacturer": Manufacturer.CROUZET,
            }
        }
    }

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"]
        if "crouzet" in vendor.lower():
            meta.global_metadata.manufacturer = Manufacturer.CROUZET
            return meta


class CrouzetXN05(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tags = { "ethernet", }

    tests = {
        "crouzet_xn05": {
            "global_metadata": {
                "manufacturer": Manufacturer.CROUZET,
                "product": "XN05  24VD",
                "revision": "V1.8",
            },
            "tags": tags,
        }
    }

    def process(self, obj, meta):
        mei_objs = obj["mei_response"]["objects"]
        vendor = mei_objs["vendor"]
        product_code = mei_objs["product_code"]
        if "crouzet" in vendor.lower() and "xn05" in product_code.lower():
            meta.global_metadata.manufacturer = Manufacturer.CROUZET
            meta.global_metadata.product = product_code.rstrip()
            meta.global_metadata.revision = mei_objs.get("revision", None)
            meta.tags = self.tags
            return meta
