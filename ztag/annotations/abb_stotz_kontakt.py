from ztag.annotation import *


class ABBStotzKontakt(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    #ttests = {
    #    "abb_stotz_kontakt": {
    #        "global_metadata": {
    #            "manufacturer": Manufacturer.ABB_STOTZ_KONTAKT,
    #        }
    #    }
    #}

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        if "abb stotz kontakt" in vendor:
            meta.global_metadata.manufacturer = Manufacturer.ABB_STOTZ_KONTAKT
            return meta
