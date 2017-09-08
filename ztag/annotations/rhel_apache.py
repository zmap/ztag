from ztag.annotation import *


class RHELDefaultApache(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        if obj["title"] == "Test Page for the Apache HTTP Server on Red Hat Enterprise Linux":
            meta.global_metadata.os = OperatingSystem.REDHAT
            return meta
