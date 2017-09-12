from ztag.annotation import *

class TIVO(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "TiVo DVR":
            meta.global_metadata.manufacturer = Manufacturer.TIVO
            meta.global_metadata.product = "DVR"
            meta.global_metadata.device_type = Type.DVR
            meta.tags.add("embedded")
            return meta

