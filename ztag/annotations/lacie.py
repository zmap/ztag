from ztag.annotation import *

class LaCie(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "LaCie&nbsp;&#124;&nbsp;Dashboard":
            meta.global_metadata.manufacturer = Manufacturer.LACIE
            meta.global_metadata.product = "Storage Device"
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta

