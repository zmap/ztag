from ztag.annotation import *

class CiscoHTTPS(TLSTag):

    protocol = protocols.HTTPS
    subprotocol = protocols.HTTPS.TLS
    port = None

    tests = {
        "cisco_ios_server":{
            "local_metadata":{
                "manufacturer":"Cisco"
            }
        }
    } 

    def process(self, obj, meta):
        cn = obj["certificate"]["parsed"]["issuer"]["common_name"][0]
        if "cisco" in cn.lower():
            meta.global_metadata.manufacturer = Manufacturer.CISCO
            meta.tags.add("embedded")
            meta.global_metadata.device_type = Type.NETWORK
            return meta
