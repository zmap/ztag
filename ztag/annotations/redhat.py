from ztag.annotation import *

class RedHatSatelite(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"].strip() == "Red Hat Satellite\n      \n      \n         - Sign In":
            meta.global_metadata.os = OperatingSystem.REDHAT
            return meta

