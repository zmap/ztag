from ztag.annotation import *


class HikvisionWebs(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if "hikvision-webs" in server.lower():
            meta.global_metadata.manufacturer = Manufacturer.HIKVISION
            meta.global_metadata.device_type = Type.CAMERA 
            meta.local_metadata.product = "Hikvision-Webs"
            return meta

