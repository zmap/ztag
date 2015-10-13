from ztag.annotation import *


class SEElectronicDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "se_electronic_g_02_90_00": {
            "global_metadata": {
                "manufacturer": Manufacturer.SE_ELECTRONIC,
            }
        }
    }

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if "se-elektronic" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.SE_ELECTRONIC
            return meta


class SEElectronicPowerController(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "se_electronic_g_02_90_00": {
            "global_metadata": {
                "manufacturer": Manufacturer.SE_ELECTRONIC,
                "product": "G 02 90 00",
                "revision": "V02.01.21",
            }
        }
    }

    MODELS = {
        "g 02 90 00"
    }

    def process(self, obj, meta):
        mei_objs = obj["mei_response"]["objects"]
        vendor = mei_objs["vendor"]
        product_code = mei_objs["product_code"]
        if "se-elektronic" not in vendor.lower():
            return
        lpc = product_code.lower()
        is_power_controller = sum([
            1 if m in lpc else 0 for m in self.MODELS
        ])
        if is_power_controller > 0:
            meta.global_metadata.manufacturer = Manufacturer.SE_ELECTRONIC
            meta.global_metadata.product = product_code.strip()
            revision = mei_objs.get("revision", "").strip()
            if revision:
                meta.global_metadata.revision = revision
            return meta
