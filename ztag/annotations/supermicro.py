from ztag.annotation import *


class SuperMicroComputer(Annotation):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        organization = obj["certificate"]["certificate"]["issuer"]["organization"][0]
        common_name = obj["certificate"]["certificate"]["issuer"]["common_name"][0]
        if organization == "Super Micro Computer" and common_name == "IPMI":
            meta.global_metadata.manufacturer = Manufacturer.SUPERMICROCOMPUTER
            meta.global_metadata.device_type = Type.IPMI
            return meta
                


