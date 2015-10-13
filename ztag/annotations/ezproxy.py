from ztag.annotation import * 


class EZProxyServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
        "ezproxy_server":{
            "local_metadata":{
                "product":"EZProxy",
                "manufacturer":"OCLC"
            }
        }
    } 

    def process(self, obj, meta):	
        server = obj["headers"]["server"]	
        if "ezproxy" in server.lower():
            meta.local_metadata.manufacturer = "OCLC"
            meta.local_metadata.product = "EZProxy"
            return meta
