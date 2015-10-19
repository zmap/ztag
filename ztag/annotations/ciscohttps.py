from ztag.annotation import *

class CiscoHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
        "cisco_ios_server":{
            "global_metadata":{
                "manufacturer":"Cisco",
                "device_type":Type.NETWORK
            },
            "tags":["embedded",]
        }
    } 

    def process(self, obj, meta):
        cn = obj["certificate"]["parsed"]["issuer"]["common_name"][0]
        if "cisco" in cn.lower():
            meta.global_metadata.manufacturer = Manufacturer.CISCO
            meta.global_metadata.device_type = Type.NETWORK
            meta.tags.add("embedded")
            return meta
