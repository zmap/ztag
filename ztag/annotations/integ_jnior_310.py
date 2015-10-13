from ztag.annotation import *


class INTEGJNIOR310(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    def process(self, obj, meta):
        vendor = obj["mei_response"]["objects"]["vendor"].lower()
        product_code = obj["mei_response"]["objects"]["product_code"].lower()
        if "integ" in vendor and "jnior" in product_code:
            meta.global_metadata.manufacturer = Manufacturer.INTEG
            meta.global_metadata.product = "JNIOR" 
            meta.global_metadata.version = product_code.split(" ")[1] 
            meta.device_type = Type.CINEMA
