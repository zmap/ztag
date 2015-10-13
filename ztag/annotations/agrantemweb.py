from ztag.annotation import Annotation
from ztag import protocols

import ztag.test

class AgranatEmWeb(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    tests = {
        "agranat_emweb":{
            "local_metadata":{
                "manufacturer":"Agranat",
                "product":"EmWeb",
                "version":"4.01"
            },
            "tags":["embedded", ]
        }
    } 

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if "agranat-emweb" in server.lower():
            meta.local_metadata.manufacturer = "Agranat"
            meta.local_metadata.product = "EmWeb"

            if "/" in server:
                version = server.split("/")[-1]
                version = version.replace("_", ".")
                version = version.replace("R", "")
                meta.local_metadata.version = version

            meta.tags.add("embedded")

            return meta

        return None
