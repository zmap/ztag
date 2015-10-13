from ztag.annotation import *

class MiniHTTPD(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    def process(self, obj, meta):
        server = d["headers"]["server"]    
        meta = self.simple_banner_version(server.split(" ", 1)[0], "mini_httpd", meta)
        if meta and " " in server:
            meta.local_metadata.revision = server.split(" ", 1)[1]
        return meta

