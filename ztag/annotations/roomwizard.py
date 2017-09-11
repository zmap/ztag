from ztag.annotation import *

class RoomWizard(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"].strip() == "RoomWizard(TM)":
            meta.global_metadata.manufacturer = Manufacturer.ROOMWIZARD
            meta.global_metadata.device_type = Type.SIGN
            meta.tags.add("embedded")
            return meta
