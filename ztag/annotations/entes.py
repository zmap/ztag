from ztag.annotation import *


class EntesMEIDevice(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tests = {
        "entes_rg_xxcs": {
            "global_metadata": {
                "manufacturer": Manufacturer.ENTES,
                "product": "RG-XXCS",
                "revision": "V4.01",
                "device_type": Type.POWER_CONTROLLER,
            }
        },
        "entes_mpr_63": {
            "global_metadata": {
                "manufacturer": Manufacturer.ENTES,
                "product": "MPR-63",
                "revision": "v1.67",
                "device_type": Type.NETWORK_ANALYZER,
            }
        }
    }

    def process(self, obj, meta):
        mei_objs = obj["mei_response"]["objects"]
        product_url = mei_objs.get("product_url", "").lower()
        vendor_url = mei_objs.get("vendor_url", "").lower()
        vendor = mei_objs.get("vendor", "").lower()
        if product_url == "www.entes.com.tr" or \
            vendor_url == "www.entes.com.tr" or \
            "entes" in vendor:
            # Set vendor always
            meta.global_metadata.manufacturer = Manufacturer.ENTES
            product = mei_objs.get("model_name", None)
            if product:
                meta.global_metadata.product = product.rstrip()
            meta.global_metadata.revision = mei_objs.get("revision", None)
            # Grab product if there
            product_name = mei_objs.get("product_name", "").lower()
            # Set device type if possible
            if 'network analyser' in product_name:
                meta.global_metadata.device_type = Type.NETWORK_ANALYZER
            elif 'power' in product_name and 'controller' in product_name:
                meta.global_metadata.device_type = Type.POWER_CONTROLLER
            elif 'power' in product_name and 'monitor' in product_name:
                meta.global_metadata.device_type = Type.POWER_MONITOR
            return meta
