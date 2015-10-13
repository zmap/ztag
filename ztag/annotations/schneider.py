from ztag.annotation import *

def _process(self, obj, meta):
    vendor = obj["mei_response"]["objects"]["vendor"].lower()
    product_code = obj["mei_response"]["objects"]["product_code"].lower()
    if "schneider electric" not in vendor \
            and "telemecanique" not in vendor:
        return
    for model in self.MODELS:
        if model in product_code:
            break
    else:
        return
    meta.global_metadata.manufacturer = Manufacturer.SCHNEIDER
    meta.global_metadata.product = obj["mei_response"]["objects"]["product_code"]
    meta.global_metadata.revision = obj["mei_response"]["objects"].get("revision", None)
    meta.global_metadata.device_type = self.DEVICE_TYPE
    meta.tags = self.TAGS
    return meta



class SchneiderElectric(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None
    TAGS = set()


class SchneiderElectricGateway(SchneiderElectric):

    MODELS = [
        "bmx p34",
        "bmx nor",
        "noe",
        "sas tsx",
        "sr3 net",
        "otb",
    ]
    DEVICE_TYPE = Type.SCADA_GATEWAY
    process = _process


class SchneiderController(SchneiderElectric):

    MODELS = [
        "hmi",
    ]

    DEVICE_TYPE = Type.SCADA_CONTROLLER
    process = _process


class ScheniderLogicController(SchneiderElectric):

    MODELS = [
        "twdl",
        "tm",
        "tsx",
    ]

    DEVICE_TYPE = Type.PLC
    process = _process


class SchneiderPowerController(SchneiderElectric):

    MODELS = [
        "nf2000",
        "pm5",
    ]

    DEVICE_TYPE = Type.POWER_CONTROLLER

    process = _process


class SchneiderCBUProcessor(SchneiderElectric):

    MODELS = [
        "cbu",
        "cpu",
    ]

    DEVICE_TYPE = Type.SCADA_CONTROLLER
    TAGS = {Type.SCADA_PROCESSOR, }

    process = _process


class SchneiderTouchscreen(SchneiderElectric):

    MODELS = [
        "hmigto",
        "hmis5t",
        "hmistu",
        "xbtgt",
        "xbt-gt",
    ]

    DEVICE_TYPE = Type.SCADA_CONTROLLER
    TAGS = {"touchscreen", }
    process = _process


class SchneiderNF3000(SchneiderElectric):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    MODELS = [
        "nf3000",
    ]

    DEVICE_TYPE = Type.LIGHT_CONTROLLER

    process = _process

    tests = {
        "schneider_nf3000": {
            "global_metadata": {
                "manufacturer": Manufacturer.SCHNEIDER,
                "product": "NF3000",
                "revision": "V05.2",
                "device_type": Type.LIGHT_CONTROLLER,
            },
        }
    }


class SchneiderMEIGeneric(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"]
        if "schneider electric" in vendor.lower():
            meta.global_metadata.manufacturer = Manufacturer.SCHNEIDER
            return meta
