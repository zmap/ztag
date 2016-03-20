from ztag.annotation import *

import re

class CherokeeServer(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    version_re = re.compile('(/[A-Za-z0-9_.(]+)')
    os_re = re.compile('\(([A-Za-z0-9_]+)\)')

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if "cherokee" in server.lower():
            meta.local_metadata.manufacturer = Manufacturer.CHEROKEE
            meta.local_metadata.product = "HTTP Server"

            version = self.version_re.search(server)
            if version and version.group(1):
                meta.local_metadata.version = version
            os = self.os_re.search(server)
            if os and os.group(1):
                if "/" in os:
                    os = os.split("/")[0]
                meta.global_metadata.os = os
            return meta

