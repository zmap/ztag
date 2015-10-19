from ztag.annotation import *

class CiscoIOSServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None
    
    tests = {
        "cisco_ios_server":{
            "global_metadata":{
                "manufacturer":"Cisco",
                "os":"IOS",
                "device_type":Type.INFRASTRUCTURE_ROUTER
            }
        }
    } 

    def process(self, obj, meta):	
        server = obj["headers"]["server"]	
        if "cisco-ios" in server.lower():
            meta.global_metadata.manufacturer = Manufacturer.CISCO
            meta.global_metadata.os = "IOS"
            meta.global_metadata.device_type = Type.INFRASTRUCTURE_ROUTER
            return meta
