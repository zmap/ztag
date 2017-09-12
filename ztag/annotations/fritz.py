from ztag.annotation import *


class FritzBoxHTTP(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "NETGEAR Web Smart Switch":
            meta.global_metadata.device_type = Type.CABLE_MODEM
            meta.global_metadata.manufacturer = Manufacturer.AVM
            meta.global_metadata.product = "FRITZ!Box"
            meta.tags.add("embedded")
            return meta

