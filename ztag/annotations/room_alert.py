from ztag.annotation import Annotation, Manufacturer, Type

from ztag import protocols


class RoomAlertMEI(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tags = [
        Type.ENVIRONMENT_MONITOR,
        Type.TEMPERATURE_MONITOR,
    ]

    def process(self, obj, meta):
        product_code = obj["mei_response"]["objects"]["product_code"].lower()
        if "room alert" in product_code:
            meta.tags = self.tags
            meta.global_metadata.manufacturer = Manufacturer.AVTECH
            meta.global_metadata.product = "Room Alert"
            meta.device_type = Type.ENVIRONMENT_MONITOR
            return meta
