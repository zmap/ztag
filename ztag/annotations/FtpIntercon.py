from ztag.annotation import Annotation
from ztag.annotation import Type
from ztag.annotation import Manufacturer
from ztag import protocols
import ztag.test
import re


class FtpIntercon(Annotation):
    name = "InterConFTP"
    protocol = protocols.FTP
    subprotocol = protocols.FTP.BANNER
    port = None

    manufact_re = re.compile(
        "^220 Intercon FTP server \(MikroTik (\d+\.\d+)\) ready",
        re.IGNORECASE
        )

    tests = {
        "FtpIntercon_1": {
            "global_metadata": {
                "manufacturer": Manufacturer.INTERCON,
                "device_type": Type.PRINT_SERVER,
            },
            "local_metadata": {
                "product": "MikroTik",
                "version": "5.26"
            }
        }
    }

    def process(self, obj, meta):
        banner = obj["banner"]

        if self.manufact_re.search(banner):
            meta.global_metadata.device_type = Type.PRINT_SERVER
            meta.global_metadata.manufacturer = Manufacturer.INTERCON

            meta.local_metadata.product = "MikroTik"

            version = self.manufact_re.search(banner).group(1)
            meta.local_metadata.version = version

            return meta

        return None
