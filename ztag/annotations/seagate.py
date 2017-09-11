from ztag.annotation import *

class SeagateRemoteAccessService(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "Welcome to SeagateShare.com Directory &amp; Remote Access Service":
            meta.global_metadata.manufacturer = Manufacturer.SEAGATE
            meta.global_metadata.product = "Home NAS"
            meta.global_metadata.device_type = Type.NAS
            meta.tags.add("embedded")
            return meta

