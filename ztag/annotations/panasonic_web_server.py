from ztag.annotation import *


class PanasonicWebServer(Annotation):

    protocol = protocols.MODBUS
    subprotocol = protocols.MODBUS.DEVICE_ID
    port = None

    tags = {"ethernet", }

    tests = {
        "panasonic_fpwebd": {
            "global_metadata": {
                "manufacturer": Manufacturer.PANASONIC,
                "product": "FP-MB-TCP",
                "version": "130730",
            },
            "local_metadata": {
                "manufacturer": Manufacturer.PANASONIC,
                "product": "FP-WebServer",
                "version": "FPWEBD",
                "revision": "V2.6",
            },
            "tags": tags,
        }
    }

    def process(self, obj, meta):
        mei_objs = obj["mei_response"]["objects"]
        vendor = mei_objs["vendor"]
        product_name = mei_objs["product_name"]
        revision = mei_objs.get("revision", "").strip()
        if "peweu" not in vendor.lower():
            return
        if "fp-webserver" not in product_name.lower():
            return None
        meta.global_metadata.manufacturer = Manufacturer.PANASONIC
        meta.local_metadata.manufacturer = Manufacturer.PANASONIC
        meta.local_metadata.product = product_name.strip()
        version = mei_objs.get("product_code", "").strip()
        if version:
            meta.local_metadata.version = version
        revision = mei_objs.get("revision", "").strip()
        if revision:
            meta.local_metadata.revision = revision
        model_name = mei_objs.get("model_name", "").strip()
        if model_name:
            meta.global_metadata.version = model_name
        app = mei_objs.get("user_application_name", "").strip()
        if app:
            meta.global_metadata.product = app
        meta.device_type = Type.SCADA_GATEWAY
        meta.tags = self.tags
        return meta
