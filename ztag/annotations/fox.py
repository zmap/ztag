from ztag.annotation import *


class FoxSCADA(Annotation):

    port = 1911
    protocol = protocols.FOX
    subprotocol = protocols.FOX.DEVICE_ID

    tests = {
        "device_with_fox": {
            "tags": [
                "scada",
                "building control",
            ],
        },
    }

    def process(self, obj, meta):
        meta.tags.add("scada")
        meta.tags.add("building control")
        return meta
