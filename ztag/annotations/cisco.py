from ztag.annotation import * 


class CiscoServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
        "cisco_server":{
            "global_metadata":{
                "manufacturer":"Cisco",
            }
        }
    } 

    def process(self, obj, meta):	
	server = obj["headers"]["server"]	
	if "cisco" in server.lower():
	    meta.global_metadata.manufacturer = "Cisco"
            return meta
