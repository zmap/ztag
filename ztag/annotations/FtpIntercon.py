from ztag.annotation import Annotation
from ztag import protocols
import ztag.test
import re


class InterConFTP(Annotation):
    name = "InterConFTP"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 Intercon FTP server \(MikroTik (\d+\.\d+)\) ready",
        re.IGNORECASE
        )

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manfact_re.search(banner):
            meta.global_metadata.device_type = Type.PRINT_SERVER
            meta.global_metadata.manufacturer = Type.INTERCON
            meta.local_metadata.product = "MikroTik"

            version = self.manufact_re.search(banner).group(1)
            meta.local_metadata.version = version
            return meta

        return None
