from ztag.annotation import *

class DellIDRACTag(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    def process(self, obj, meta):
        s = obj["certificate"]["parsed"]
        if s["organizational_unit"][0] == "Remote Access Group" \
                and s["organization"][0] == "Dell Inc.":
            meta.global_metadata.device_type = Type.IPMI
            meta.global_metadata.manufacturer = Manufacturer.DELL
            meta.global_metadata.product = "iDRAC"
            return meta
