from ztag.annotation import *


class FoxBrand(Annotation):

    port = 20000
    protocol = protocols.FOX
    subprotocol = protocols.FOX.DEVICE_ID

    _vendors = [
        ("vykon", Manufacturer.VYKON, Type.SCADA_CONTROLLER),
        ("facexp", Manufacturer.FACEXP, Type.SCADA_CONTROLLER),
    ]


    def process(self, obj, meta):
        vendor = obj["vendor_id"].lower().strip()
        for v in _vendors:
            if vendors.startswith(v[0]):
                meta.global_metadata.manufacturer = v[1]
                meta.global_metadata.device_type = v[2]
                return meta
