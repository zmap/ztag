from ztag.annotation import *


class LantronixMEIDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "lantronix_xport": {
            "global_metadata": {
                "manufacturer": Manufacturer.LANTRONIX,
            }
        }
    }

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if "lantronix" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.LANTRONIX
            return meta


class LantronixXPort(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tags = {"ethernet", }

    tests = {
        "lantronix_xport": {
            "global_metadata": {
                "manufacturer": Manufacturer.LANTRONIX,
                "product": "XPort",
                "revision": "V3.3.0.1GC",
                "device_type": Type.SCADA_GATEWAY,
            },
            "tags": tags,
        }
    }

    def process(self, obj, meta):
        mei_objs = obj["mei_response"]["objects"]
        vendor = mei_objs["vendor"]
        product_code = mei_objs["product_code"]
        if "lantronix" in vendor.lower() \
                and "xport" in product_code.lower():
            meta.global_metadata.manufacturer = Manufacturer.LANTRONIX
            meta.global_metadata.product = product_code.rstrip()
            revision = mei_objs.get("revision", "").strip()
            if revision:
                meta.global_metadata.revision = revision
            meta.global_metadata.device_type = Type.SCADA_GATEWAY
            meta.tags = self.tags
            return meta
