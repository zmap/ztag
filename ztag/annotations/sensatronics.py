from ztag.annotation import *


class SensatronicsEnvMon(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        t = obj["title"].strip()
        if t.startswith("Environmental Monitor") \
                or t.startswith("IT Temperature Monitor") \
                or t.startswith("Universal Temperature Monitor"):
            if "Sensatronics" in obj["body"]:
                meta.global_metadata.device_type = Type.ENVIRONMENT_MONITOR
                meta.global_metadata.manufacturer = Manufacturer.SENSATRONICS
                meta.tags.add("embedded")
                meta.tags.add("scada")
                return meta

