from ztag.annotation import *

class HDHomeRun(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "HDHomeRun Main Menu":
            meta.global_metadata.manufacturer = "SiliconDust"
            meta.global_metadata.product = "HDHomeRun"
            meta.global_metadata.device_type = Type.TV_TUNER
            meta.tags.add("embedded")
            return meta

