from ztag.annotation import * 

import re


class Helix(Annotation):

    protocol = protocols.HTTP
    subprotocol = protocols.HTTP.GET
    port = None

    version_re = re.compile(
        "^Helix Mobile Server/(\d+(\.\d+)*)",
        re.IGNORECASE
        )

    os_re = re.compile(
        "^Helix Mobile Server/(?:\d+(?:\.\d+)*) \(.*\)",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        server = obj["headers"]["server"]
        if server.startswith("Helix Mobile Server"):
            meta.local_metadata.product = "Helix Mobile Server"

            version = self.version_re.search(server).group(1)
            meta.local_metadata.version = version

            os = self.os_re.search(server).group(1)
            if "win" in os:
                meta.global_metadata.os = OperatingSystem.WINDOWS
            elif "rhel4" in os:
                meta.global_metadata.os = OperatingSystem.REDHAT
                meta.global_metadata.os_version = "4"
            elif "rhel5" in os:
                meta.global_metadata.os = OperatingSystem.REDHAT
                meta.global_metadata.os_version = "5"
            elif "rhel6" in os:
                meta.global_metadata.os = OperatingSystem.REDHAT
                meta.global_metadata.os_version = "6"
