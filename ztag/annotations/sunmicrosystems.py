from ztag.annotation import *


class SunMicroSystems(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = obj["certificate"]["parsed"]["issuer"]["organization"][0]
        common_name = obj["certificate"]["parsed"]["issuer"]["common_name"][0]
        if "Sun Microsystems" in organization:
            meta.global_metadata.manufacturer = Manufacturer.SUN_MICROSYSTEMS
            return meta
                


